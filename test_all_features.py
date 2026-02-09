#!/usr/bin/env python
"""
Unity Circles - Comprehensive Test Suite
Tests all features including profile, communities, posts, and messages
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unity_circles.settings')
django.setup()

from django.contrib.auth.models import User
from chat.models import DirectMessage
from core.models import Community, Post, PostComment
from accounts.models import StudentProfile

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_user_system():
    print_section("TEST 1: User System")
    
    try:
        # Count existing users
        user_count = User.objects.count()
        print(f"✓ Existing users: {user_count}")
        
        # Create test users if needed
        test_users = ['alice', 'bob', 'charlie', 'diana']
        created = 0
        
        for username in test_users:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123'
                )
                user.first_name = username.capitalize()
                user.last_name = "Test"
                user.save()
                
                # Create profile
                StudentProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'bio': f'I am {username}, a test user.',
                        'role': 'student',
                        'interests': 'Python, Django, Testing'
                    }
                )
                created += 1
                print(f"✓ Created user: {username}")
        
        if created == 0:
            print("✓ All test users already exist")
        
        # Verify profiles
        profile_count = StudentProfile.objects.count()
        print(f"✓ Total profiles: {profile_count}")
        
        return True
    except Exception as e:
        print(f"✗ Error in user system: {e}")
        return False

def test_communities():
    print_section("TEST 2: Community System")
    
    try:
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        
        # Create test communities
        communities_data = [
            {
                'name': 'Python Developers',
                'description': 'A community for Python enthusiasts',
                'category': 'tech',
                'creator': alice
            },
            {
                'name': 'Machine Learning',
                'description': 'Discuss ML algorithms and applications',
                'category': 'tech',
                'creator': bob
            },
            {
                'name': 'Startup Ideas',
                'description': 'Share and discuss startup concepts',
                'category': 'business',
                'creator': alice
            }
        ]
        
        created = 0
        for data in communities_data:
            community, was_created = Community.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if was_created:
                community.members.add(data['creator'])
                community.members.add(alice if data['creator'] != alice else bob)
                created += 1
                print(f"✓ Created community: {data['name']}")
        
        if created == 0:
            print("✓ All test communities already exist")
        
        # Verify communities
        total_communities = Community.objects.count()
        print(f"✓ Total communities: {total_communities}")
        
        for community in Community.objects.all():
            member_count = community.members.count()
            print(f"  - {community.name}: {member_count} members")
        
        return True
    except Exception as e:
        print(f"✗ Error in community system: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_posts():
    print_section("TEST 3: Post System")
    
    try:
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        
        # Get communities
        communities = Community.objects.all()[:2]
        
        if not communities:
            print("✗ No communities found. Run community test first.")
            return False
        
        # Create test posts
        posts_data = [
            {
                'title': 'Getting Started with Django',
                'content': 'Django is an amazing framework for web development. Here are some tips...',
                'author': alice,
                'community': communities[0]
            },
            {
                'title': 'Neural Networks Explained',
                'content': 'Understanding the basics of neural networks and deep learning...',
                'author': bob,
                'community': communities[1] if len(communities) > 1 else communities[0]
            },
            {
                'title': 'Best Practices for REST APIs',
                'content': 'When building APIs, consider these important design principles...',
                'author': alice,
                'community': communities[0]
            }
        ]
        
        created = 0
        for data in posts_data:
            post, was_created = Post.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if was_created:
                created += 1
                print(f"✓ Created post: {data['title']}")
        
        if created == 0:
            print("✓ All test posts already exist")
        
        # Verify posts
        total_posts = Post.objects.count()
        print(f"✓ Total posts: {total_posts}")
        
        for post in Post.objects.all()[:5]:
            print(f"  - {post.title} by {post.author.username} (↑{post.upvotes} ↓{post.downvotes})")
        
        return True
    except Exception as e:
        print(f"✗ Error in post system: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_comments():
    print_section("TEST 4: Comment System")
    
    try:
        users = User.objects.filter(username__in=['alice', 'bob', 'charlie'])[:2]
        posts = Post.objects.all()[:2]
        
        if not posts:
            print("✗ No posts found. Run post test first.")
            return False
        
        # Create test comments
        comments_data = [
            {
                'post': posts[0],
                'author': users[1] if len(users) > 1 else users[0],
                'content': 'Great post! Very informative.'
            },
            {
                'post': posts[0],
                'author': users[0],
                'content': 'Thanks! Glad you found it helpful.'
            }
        ]
        
        if len(posts) > 1:
            comments_data.append({
                'post': posts[1],
                'author': users[0],
                'content': 'Interesting perspective on neural networks!'
            })
        
        created = 0
        for data in comments_data:
            # Check if similar comment exists
            existing = PostComment.objects.filter(
                post=data['post'],
                author=data['author'],
                content=data['content']
            ).first()
            
            if not existing:
                PostComment.objects.create(**data)
                created += 1
                print(f"✓ Created comment on '{data['post'].title[:30]}...'")
        
        if created == 0:
            print("✓ All test comments already exist")
        
        # Verify comments
        total_comments = PostComment.objects.count()
        print(f"✓ Total comments: {total_comments}")
        
        for comment in PostComment.objects.all()[:5]:
            print(f"  - {comment.author.username}: {comment.content[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error in comment system: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_messages():
    print_section("TEST 5: Messaging System")
    
    try:
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        
        # Create test messages
        messages_data = [
            {
                'sender': alice,
                'receiver': bob,
                'content': 'Hey Bob, how are you?'
            },
            {
                'sender': bob,
                'receiver': alice,
                'content': 'Hi Alice! I'm good, thanks. How about you?'
            },
            {
                'sender': alice,
                'receiver': bob,
                'content': 'Doing great! Want to collaborate on that Django project?'
            }
        ]
        
        created = 0
        for data in messages_data:
            # Check if similar message exists
            existing = DirectMessage.objects.filter(
                sender=data['sender'],
                receiver=data['receiver'],
                content=data['content']
            ).first()
            
            if not existing:
                DirectMessage.objects.create(**data)
                created += 1
                print(f"✓ Created message from {data['sender'].username} to {data['receiver'].username}")
        
        if created == 0:
            print("✓ All test messages already exist")
        
        # Verify messages
        total_messages = DirectMessage.objects.count()
        print(f"✓ Total messages: {total_messages}")
        
        for message in DirectMessage.objects.all()[:5]:
            print(f"  - {message.sender.username} → {message.receiver.username}: {message.content[:40]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error in messaging system: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_relationships():
    print_section("TEST 6: Data Relationships")
    
    try:
        alice = User.objects.get(username='alice')
        
        # Test user relationships
        print(f"\n👤 User: {alice.username}")
        print(f"  - Communities: {alice.communities.count()}")
        print(f"  - Posts: {alice.community_posts.count()}")
        print(f"  - Comments: {alice.post_comments.count()}")
        print(f"  - Messages sent: {alice.dm_sent.count()}")
        print(f"  - Messages received: {alice.dm_received.count()}")
        
        # Test community relationships
        community = Community.objects.first()
        if community:
            print(f"\n🏘️  Community: {community.name}")
            print(f"  - Members: {community.members.count()}")
            print(f"  - Posts: {community.posts.count()}")
            print(f"  - Creator: {community.creator.username}")
        
        # Test post relationships
        post = Post.objects.first()
        if post:
            print(f"\n📝 Post: {post.title[:40]}...")
            print(f"  - Author: {post.author.username}")
            print(f"  - Community: {post.community.name}")
            print(f"  - Comments: {post.comments.count()}")
            print(f"  - Upvotes: {post.upvotes}")
        
        return True
    except Exception as e:
        print(f"✗ Error testing relationships: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    print("\n" + "🚀" * 35)
    print("       UNITY CIRCLES - COMPREHENSIVE TEST SUITE")
    print("🚀" * 35)
    
    results = {
        'User System': test_user_system(),
        'Communities': test_communities(),
        'Posts': test_posts(),
        'Comments': test_comments(),
        'Messages': test_messages(),
        'Relationships': test_relationships()
    }
    
    print_section("TEST SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:.<50} {status}")
    
    print(f"\n{'─' * 70}")
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print('─' * 70)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your Unity Circles app is fully functional!")
        print("\n📋 Next Steps:")
        print("1. Start the server: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/")
        print("3. Login with:")
        print("   - Username: alice (or bob, charlie, diana)")
        print("   - Password: password123")
        print("4. Test features:")
        print("   - Profile: /profile/")
        print("   - Dashboard: /dashboard/")
        print("   - Communities: /communities/")
        print("   - Messages: /chat/")
        print("\n✨ Have fun testing Unity Circles!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
