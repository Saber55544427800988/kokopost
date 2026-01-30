import json

# Test lesson data structure
test_lesson = {
    "topic": "Ordering Food",
    "language": "Spanish",
    "slide1": {
        "english_topic": "Ordering Food",
        "target_language": "Spanish"
    },
    "slide2": {
        "vocab": [
            {"word": "Menú", "meaning": "Menu"},
            {"word": "Cuenta", "meaning": "Bill"},
            {"word": "Camarero", "meaning": "Waiter"}
        ]
    },
    "slide3": {
        "examples": [
            {"phrase": "Quisiera el menú", "meaning": "I would like the menu"},
            {"phrase": "La cuenta, por favor", "meaning": "The bill, please"},
            {"phrase": "¿Qué recomienda?", "meaning": "What do you recommend?"}
        ]
    },
    "audio_script": [
        {"voice": "en", "text": "Today we're learning about Ordering Food. Let's learn some Spanish!"},
        {"voice": "en", "text": "First word: Menu. In Spanish:"},
        {"voice": "native", "text": "Menú"},
        {"voice": "en", "text": "Second word: Bill. In Spanish:"},
        {"voice": "native", "text": "Cuenta"},
        {"voice": "en", "text": "Third word: Waiter. In Spanish:"},
        {"voice": "native", "text": "Camarero"},
        {"voice": "en", "text": "Now some examples. Number one:"},
        {"voice": "native", "text": "Quisiera el menú"},
        {"voice": "en", "text": "Number two:"},
        {"voice": "native", "text": "La cuenta, por favor"},
        {"voice": "en", "text": "And number three:"},
        {"voice": "native", "text": "¿Qué recomienda?"},
        {"voice": "en", "text": "Great job! Keep practicing with Koko Teacher!"}
    ]
}

# Validate structure
print("✅ Testing Lesson Data Structure...")
print(f"   Topic: {test_lesson['slide1']['english_topic']}")
print(f"   Language: {test_lesson['language']}")
print(f"   Vocabulary items: {len(test_lesson['slide2']['vocab'])}")
print(f"   Example phrases: {len(test_lesson['slide3']['examples'])}")
print(f"   Audio segments: {len(test_lesson['audio_script'])}")

# Check format compliance
errors = []

# Check vocab count
if len(test_lesson['slide2']['vocab']) != 3:
    errors.append("❌ Vocabulary must have exactly 3 items")
else:
    print("   ✓ Vocabulary: 3 items")

# Check examples count
if len(test_lesson['slide3']['examples']) != 3:
    errors.append("❌ Examples must have exactly 3 items")
else:
    print("   ✓ Examples: 3 items")

# Check audio script
if len(test_lesson['audio_script']) < 10:
    errors.append("❌ Audio script too short")
else:
    print("   ✓ Audio script: adequate length")

# Check for required keys
required_keys = ['word', 'meaning']
for i, item in enumerate(test_lesson['slide2']['vocab']):
    for key in required_keys:
        if key not in item:
            errors.append(f"❌ Vocab item {i+1} missing '{key}'")

required_keys = ['phrase', 'meaning']
for i, item in enumerate(test_lesson['slide3']['examples']):
    for key in required_keys:
        if key not in item:
            errors.append(f"❌ Example item {i+1} missing '{key}'")

if errors:
    print("\n⚠️  Format Issues Found:")
    for error in errors:
        print(f"   {error}")
else:
    print("\n✅ All format checks passed!")
    print("\n📋 Sample Output:")
    print(f"\nSlide 1:")
    print(f"  Topic: {test_lesson['slide1']['english_topic']}")
    print(f"  Learning: {test_lesson['slide1']['target_language']}")
    print(f"\nSlide 2 (Vocabulary):")
    for i, item in enumerate(test_lesson['slide2']['vocab']):
        print(f"  {i+1}. {item['word']} = {item['meaning']}")
    print(f"\nSlide 3 (Examples):")
    for i, item in enumerate(test_lesson['slide3']['examples']):
        print(f"  {i+1}. {item['phrase']} ({item['meaning']})")

print("\n✅ Format validation complete!")
