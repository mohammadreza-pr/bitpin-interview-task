from django.core.management.base import BaseCommand
from django.conf import settings
from confluent_kafka import Consumer
from collections import defaultdict
import json
from content.models import Rate, Content
from django.db import transaction

class Command(BaseCommand):
    help = 'Consume ratings from Kafka'

    def setup_kafka(self):
        kafka_consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BROKER_URL,
            'group.id': 'rating_consumers',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True,
            'auto.commit.interval.ms': 5000
        })
        kafka_consumer.subscribe([settings.KAFKA_TOPIC_RATINGS])
        return kafka_consumer
    
    def handle(self, *args, **kwargs):
        kafka_consumer = self.setup_kafka()
        try:
            while True:
                messages = kafka_consumer.consume(
                    num_messages=settings.KAFKA_RATINGS_CONSUMER_BATCH_SIZE,
                    timeout=1.0
                )

                if not messages:
                    continue

                self.process_rates(messages, kafka_consumer)

        finally:
            kafka_consumer.close()
    
    
    def process_rates(self, messages, consumer):
        new_rates = []
        old_rates = []
        contents_need_update = defaultdict(lambda: {'count': 0, 'sum': 0, 'weight': 0})
        for msg in messages:
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
            
            message = json.loads(msg.value().decode('utf-8'))
            user_id = message['user_id']
            post_id = message['post_id']
            score = message['score']
            weight = message['weight']
            

            current_rate = Rate.objects.filter(user_id=user_id, post_id=post_id).first()

            if current_rate:
                if current_rate in old_rates:
                    continue
                if not score == current_rate.score:
                    add_on = (score * weight) - (current_rate.score * current_rate.weight)
                    dif_of_weight = weight - current_rate.weight
                    current_rate.score = score
                    current_rate.weight = weight
                    old_rates.append(current_rate)
                    contents_need_update[post_id]['sum'] += add_on
                    contents_need_update[post_id]['weight'] += dif_of_weight
                else:
                    continue
            else:
                new_rate = Rate(user_id=user_id, post_id=post_id, score=score, weight=weight)
                if new_rate in new_rates:
                    continue
                new_rates.append(new_rate)
                contents_need_update[post_id]['sum'] += score * weight
                contents_need_update[post_id]['weight'] += weight
                contents_need_update[post_id]['count'] += 1
        
        with transaction.atomic():
            if new_rates:
                Rate.objects.bulk_create(new_rates)
            if old_rates:
                Rate.objects.bulk_update(old_rates, ['score', 'weight'])
            
            for content_id, data in contents_need_update.items():
                content = Content.objects.get(id=content_id)
                new_average = (content.total_weight * content.average_score + data['sum']) / (content.total_weight + data['weight'])
                content.average_score = new_average
                content.total_votes += data['count']
                content.total_weight += data['weight']
                content.save()

        consumer.commit(asynchronous=False)
        self.stdout.write(self.style.SUCCESS(f'Processed batch of {len(messages)} messages'))