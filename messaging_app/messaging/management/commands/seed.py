import random
import uuid
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from messaging.models import ChatUser, Conversation, Message, Notification, MessageHistory


class Command(BaseCommand):
    help = "Seed the database with realistic ChatUser, Conversation, and Message data"

    def handle(self, *args, **options):
        seed_data()
# Extensive lists of unique, natural-sounding first names with Kenyan/African influence
first_names = [
    "John", "Allan", "Peter", "David", "James", "Mary", "Jane", "Sarah", "Joseph", "Grace",
    "Michael", "Esther", "Paul", "Ruth", "Daniel", "Elizabeth", "Thomas", "Faith", "Andrew", "Joy",
    "Simon", "Ann", "Stephen", "Lucy", "Patrick", "Rose", "George", "Margaret", "Charles", "Beatrice",
    "Robert", "Catherine", "Victor", "Agnes", "Samuel", "Dorothy", "Timothy", "Patricia", "Moses", "Nancy",
    "Isaac", "Susan", "Ezekiel", "Florence", "Benjamin", "Mercy", "Elijah", "Caroline", "Aaron", "Hope",
    "Joshua", "Rebecca", "Matthew", "Hannah", "Mark", "Julia", "Luke", "Priscilla", "Philip", "Deborah",
    "Nathan", "Rachel", "Gabriel", "Helen", "Samuel", "Judith", "Emmanuel", "Lydia"
]
last_names = [
    "Kiprono", "Wambui", "Ochieng", "Abdalla", "Mwangi", "Chebet", "Njoroge", "Otieno", "Karanja", "Muthoni",
    "Omondi", "Kiptoo", "Wanjala", "Abdi", "Omolo", "Koech", "Ruto", "Lutta", "Masinde", "Oketch",
    "Simiyu", "Tarus", "Were", "Yego", "Zablon", "Cheruiyot", "Langat", "Maiyo", "Sigei", "Too",
    "Barasa", "Kimutai", "Limo", "Maritim", "Rotich", "Sang", "Towett", "Yator", "Bett", "Choge",
    "Korir", "Lagat", "Mitei", "Ngeny", "Saitoti", "Tung", "Vundi", "Wekesa", "Yuda", "Zerua",
    "Arusei", "Biwott", "Chepkwony", "Kiptalam", "Lel", "Mibei", "Rotich", "Soi", "Talam", "Yego",
    "Kemboi", "Chege", "Onyango", "Mukami", "Kibet", "Wanjohi", "Odongo", "Atieno", "Kinyanjui", "Mbugua"
]
counties = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Nyeri", "Machakos", "Kakamega", "Meru", "Kitale",
    "Kisii", "Thika", "Kericho", "Bungoma", "Embu", "Garissa", "Homa Bay", "Kilifi", "Lamu", "Mandera",
    "Narok", "Naivasha", "Vihiga", "Siaya", "Trans Nzoia", "Uasin Gishu", "West Pokot", "Taita Taveta", "Kwale",
    "Bomet", "Busia", "Isiolo", "Marsabit", "Nyandarua", "Samburu", "Turkana", "Wajir", "Laikipia"
]
occupations = [
    "Teacher", "Farmer", "Entrepreneur", "Nurse", "Driver", "Engineer", "Shopkeeper", "Chef", "Artist", "Lawyer",
    "Doctor", "Mechanic", "Tailor", "Carpenter", "Fisherman", "Trader", "Student", "Pilot", "Journalist", "Policeman",
    "IT Specialist", "Accountant", "Veterinarian", "Photographer", "Tour Guide", "Marketer", "Electrician", "Plumber",
    "Software Developer", "HR Manager", "Banker", "Consultant", "Designer", "Event Planner", "Data Analyst"
]
landmarks = ["Nairobi National Park", "Diani Beach", "Lake Nakuru", "Mount Kenya", "Masai Mara", "Amboseli", "Lamu Island", "Hell’s Gate", "Aberdare Ranges", "Tsavo", "Lake Victoria"]
teams = ["Gor Mahia", "AFC Leopards", "Harambee Stars", "Sofapaka", "Tusker FC", "Mathare United", "Bandari FC"]
foods = ["nyama choma", "ugali", "sukuma wiki", "mandazi", "chapati", "githeri", "pilau", "mutura", "kuku choma", "viazi karai", "samosa"]

# Generate 550 users with detailed profiles
def create_users():
    users = []
    for i in range(550):
        unique_first = first_names[i % len(first_names)]
        unique_last = last_names[i % len(last_names)]
        user = ChatUser(
            username=f"user{i+1}_{unique_first}{unique_last}",
            email=f"user{i+1}_{unique_first}{unique_last}@kenya.co.ke",
            first_name=unique_first,
            last_name=unique_last,
            phone_number=f"+2547{random.randint(0,9)}{random.randint(0,9)}{random.randint(100000,999999)}",
            bio=f"Jambo! I’m {unique_first} {unique_last} from {random.choice(counties)}, a {random.choice(occupations)}. I love eating {random.choice(foods)} and visiting {random.choice(landmarks)}. Born on {timezone.now().date() - timedelta(days=random.randint(365*18, 365*70))}. I’m a die-hard {random.choice(teams)} fan and work {random.choice(['remotely', 'in Nairobi', 'in the field', 'from Mombasa', 'in Kisumu', 'in Nakuru'])}. My hobbies include {random.choice(['running', 'dancing', 'reading', 'cooking', 'swimming', 'painting'])}, and I dream of traveling to {random.choice(['Jinja', 'Dar es Salaam', 'Cape Town', 'Kigali', 'Addis Ababa'])}.",
            password=make_password("testPass123")  # Uniform password for testing
        )
        user.save()
        users.append(user)
    return users

# Create 300 conversations with diverse participants
def create_conversations(users):
    conversations = []
    for _ in range(300):
        participants = random.sample(users, k=random.randint(2, 25))  # 2 to 25 participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversations.append(conversation)
    return conversations

# Generate 150-300 messages per conversation with lengthy, detailed content
def create_messages(users, conversations):
    messages = []
    greetings = ["Jambo", "Habari", "Sasa", "Karibu", "Asante", "Moin", "Salamu", "Heshima", "Shikamoo", "Mambo"]
    topics = [
        "How’s the matatu traffic today on Uhuru Highway?", "Let’s plan a nyama choma outing this weekend near Masai Mara!",
        "Nairobi rains are causing floods, stay safe everyone!", "Who’s got the latest Safcom bundles or Airtel deals?",
        "BBI debate is heating up, what’s your opinion?", "Matatu fares are up again, should we switch to boda bodas?",
        "Let’s visit Diani Beach for a team getaway!", "Ugali recipe swap—share your best tips!",
        "Kenyan music hits this week—check out Nameless’s new track!", "Power outage in Eldoret, any updates?"
    ]
    for conversation in conversations:
        participants = conversation.participants.all()
        for _ in range(random.randint(150, 300)):  # 150 to 300 messages per conversation
            sender = random.choice(participants)
            receiver = random.choice([p for p in participants if p != sender])
            message_content = f"{random.choice(greetings)}, {receiver.first_name} {receiver.last_name} and all! {random.choice(topics)} " \
                            f"I’m currently at {random.choice(counties)} near {random.choice(landmarks)}, enjoying {random.choice(foods)} with my family. " \
                            f"The weather is {random.choice(['sunny', 'rainy', 'cloudy', 'windy'])} with a temperature around {random.randint(15, 30)}°C. " \
                            f"I’ve been working on {random.choice(['a software project', 'a farm expansion', 'a business proposal'])} and need your input on {random.choice(['budgeting', 'marketing strategies', 'logistics planning'])}. " \
                            f"Last time we met, we discussed {random.choice(teams)}’s last match—their defense was weak! " \
                            f"Please call me at {sender.phone_number[-8:]} to brainstorm solutions. Looking forward to your detailed feedback! - {sender.first_name} {sender.last_name}"
            message = Message(
                message_id=uuid.uuid4(),
                conversation=conversation,
                sender=sender,
                receiver=receiver,
                message_content=message_content,
                timestamp=timezone.now() - timedelta(days=random.randint(1, 365), minutes=random.randint(0, 1440)),
                read=random.choice([True, False, False, False, False])  # Mostly unread
            )
            message.save()
            messages.append(message)
            # Create notification
            Notification.objects.create(
                notification_id=uuid.uuid4(),
                user=receiver,
                message=message
            )
            # Randomly edit some messages with history
            if random.choice([True, False, False, False, False]):
                old_content = message.message_content[:250]  # Truncate to max_length=250 for MessageHistory
                message.edited = True
                message.message_content += f" (Edited: Added {random.choice(['urgent', 'fun', 'sad', 'happy', 'important'])} note at {timezone.now().time()})"
                message.save()
                MessageHistory.objects.create(
                    message_history_id=uuid.uuid4(),
                    message=message,
                    old_content=old_content,
                    edited_by=sender
                )
            # Randomly add replies with detailed content
            if random.choice([True, False, False, False]):
                parent = random.choice(messages)
                reply_content = f"Reply to {parent.sender.first_name} {parent.sender.last_name}: Thanks for the update! I’m in {random.choice(counties)} now, " \
                              f"and things are {random.choice(['calm', 'chaotic', 'busy'])}. I agree on {random.choice(['budgeting', 'marketing strategies', 'logistics planning'])}— " \
                              f"let’s meet at {random.choice(landmarks)} to finalize plans. Weather here is {random.choice(['sunny', 'rainy', 'cloudy'])}. - {receiver.first_name}"
                reply = Message(
                    message_id=uuid.uuid4(),
                    conversation=conversation,
                    sender=receiver,
                    receiver=sender,
                    message_content=reply_content,
                    timestamp=message.timestamp + timedelta(minutes=random.randint(1, 120)),
                    parent_message=parent,
                    read=random.choice([True, False])
                )
                reply.save()
                messages.append(reply)
                Notification.objects.create(
                    notification_id=uuid.uuid4(),
                    user=sender,
                    message=reply
                )
    return messages

# Seed the database with large-scale, bulky data
def seed_data():
    print("Seeding 550 users...")
    users = create_users()
    print("Seeding 300 conversations...")
    conversations = create_conversations(users)
    print("Seeding 45000-90000 messages...")
    create_messages(users, conversations)
    print(f"Seeding complete! Total users: {ChatUser.objects.count()}, Conversations: {Conversation.objects.count()}, Messages: {Message.objects.count()}")

if __name__ == "__main__":
    seed_data()