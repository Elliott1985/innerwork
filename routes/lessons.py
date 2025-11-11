from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Purchase, Enrollment

lessons_bp = Blueprint("lessons", __name__, url_prefix="/lessons")

# Mock lesson data for each course
# Each course has multiple lessons with title and content
lesson_data = {
    1: [  # Course 1: I Am Not My Trauma
        {
            "id": 1,
            "title": "Lesson 1: Understanding Trauma",
            "content": """Welcome to the first lesson of your healing journey. Trauma is not what happens to us—it's what happens inside us as a result of what happened to us. 

In this foundational lesson, we'll explore:
• The true definition of trauma and its many forms
• How trauma affects our nervous system and daily life
• Why awareness is the crucial first step toward healing
• Common myths about trauma that we need to unlearn

Remember: You are not your trauma. You are a whole person who experienced something difficult. This distinction is the cornerstone of everything we'll build together."""
        },
        {
            "id": 2,
            "title": "Lesson 2: The Body Remembers",
            "content": """Our bodies are brilliant storytellers, holding memories our conscious minds may have tucked away for protection.

Today we'll discover:
• How trauma lives in the body, not just the mind
• Physical symptoms that emerge from emotional wounds
• The connection between chronic tension and past experiences
• Simple somatic awareness exercises to begin reconnection

The body doesn't lie. When we learn its language, we gain profound insights into our healing path. Let's begin listening with compassion."""
        },
        {
            "id": 3,
            "title": "Lesson 3: Emotional Reframing",
            "content": """The stories we tell ourselves shape our reality. Today, we practice the transformative art of reframing.

Key concepts we'll explore:
• Separating identity from experience ("I am" vs "I experienced")
• Challenging the inner critic with gentle curiosity
• Building a vocabulary of self-compassion
• Creating new neural pathways through intentional thought patterns

Healing happens when we shift from "I am broken" to "I am healing." This isn't positive thinking—it's accurate thinking. You are actively choosing growth in this very moment."""
        },
        {
            "id": 4,
            "title": "Lesson 4: Moving Forward",
            "content": """Healing isn't linear—it's a spiral. Some days you'll feel strong, others vulnerable. Both are valid parts of your journey.

In our final lesson, we'll integrate:
• Daily practices for continued emotional wellness
• How to recognize and celebrate progress (even small wins)
• Building a sustainable self-care routine
• Resources and support for the road ahead
• Creating your personal healing commitment

You've done remarkable work in this course. As you move forward, remember: healing is not about returning to who you were before. It's about becoming who you're meant to be."""
        },
    ],
    2: [  # Course 2: I'm Sorry Is No Longer an Option
        {
            "id": 1,
            "title": "Lesson 1: The Sorry Habit",
            "content": """Do you find yourself apologizing for existing? For taking up space? For having needs?

Today we examine:
• Why over-apologizing is actually a trauma response
• The difference between genuine apology and reflexive appeasement
• Cultural and gender conditioning around saying sorry
• How chronic apologizing diminishes your voice and presence

This week's practice: Notice every time you say "I'm sorry." Ask yourself: "Am I actually sorry, or am I just uncomfortable?"

You have nothing to apologize for simply by being human."""
        },
        {
            "id": 2,
            "title": "Lesson 2: Understanding Boundaries",
            "content": """Boundaries aren't walls—they're the doors and windows that let you decide who and what gets access to your energy.

We'll explore:
• What healthy boundaries actually look like
• The difference between boundaries and ultimatums
• Why saying "no" is a complete sentence
• Identifying your personal boundary markers

Boundaries aren't selfish. They're the foundation of authentic relationships. When you honor your limits, you teach others how to honor them too."""
        },
        {
            "id": 3,
            "title": "Lesson 3: The No Script",
            "content": """Saying no without apologizing feels impossible—until you practice.

Today's toolbox includes:
• Scripts for common boundary violations
• How to say no with kindness but firmness
• Dealing with pushback and manipulation
• Role-playing difficult conversations
• The power of the pause before responding

Sample script: "I appreciate you thinking of me, but that doesn't work for me right now."
No explanation needed. No apology required."""
        },
        {
            "id": 4,
            "title": "Lesson 4: Guilt vs. Growth",
            "content": """Setting boundaries will trigger guilt. That's normal—and it doesn't mean you're doing something wrong.

Final integration:
• Understanding healthy guilt vs. manipulated guilt
• Sitting with discomfort without backtracking
• Celebrating boundary wins (even small ones)
• Building a support system that respects your growth
• Long-term maintenance of your newfound voice

The guilt you feel when setting boundaries is proof that you're breaking old patterns. Feel it. Honor it. Then keep going anyway.

You are allowed to take up space."""
        },
        {
            "id": 5,
            "title": "Lesson 5: Maintaining Your Boundaries",
            "content": """Setting boundaries once isn't enough—they require ongoing maintenance and reinforcement.

Advanced concepts:
• Recognizing boundary testing behaviors
• Dealing with repeat offenders
• When to hold firm vs. when to reassess
• Creating consequences that stick
• Self-care after boundary conflicts

Remember: People who truly respect you will respect your boundaries. Those who don't are showing you who they are. Believe them."""
        },
        {
            "id": 6,
            "title": "Lesson 6: Boundaries as Self-Love",
            "content": """This journey culminates in a powerful truth: boundaries are the highest form of self-love.

Final reflections:
• Your transformation throughout this course
• Creating a boundary bill of rights for yourself
• Building sustainable practices moving forward
• Connecting boundaries to your core values
• Your commitment to continued growth

You came here apologizing for everything. You're leaving knowing that your needs, feelings, and existence require no apology.

Stand tall. Take up space. You've earned it."""
        },
    ],
    3: [  # Course 3: Heart & Mind Connection
        {
            "id": 1,
            "title": "Lesson 1: Beyond the Mind-Body Split",
            "content": """Western culture taught us to separate thinking from feeling. But indigenous wisdom and modern neuroscience agree: they were always one.

Today's exploration:
• The myth of pure rationality
• How emotions inform (not cloud) decisions
• The intelligence of the heart—literally and metaphorically
• Integrative approaches to wholeness

Your heart has wisdom your mind hasn't learned yet. Let's learn to listen."""
        },
        {
            "id": 2,
            "title": "Lesson 2: Emotional Literacy",
            "content": """Most of us were never taught the full emotional vocabulary. We default to "fine," "good," or "stressed."

Building emotional fluency:
• Expanding your feeling vocabulary beyond basics
• The nuance between similar emotions (anxious vs. concerned vs. worried)
• Physical sensations as emotional information
• Journaling exercises for deeper awareness

The more precisely you can name what you feel, the more power you have to respond skillfully."""
        },
        {
            "id": 3,
            "title": "Lesson 3: Mindful Integration Practices",
            "content": """Theory becomes transformation through practice. Today we introduce techniques to bridge heart and mind.

Practical tools:
• Heart-centered breathing meditation
• Body scan with emotional awareness
• Loving-kindness practice for self and others
• Mindful movement (gentle yoga, walking meditation)

These aren't just nice ideas—they're neuroplasticity in action. Each practice reshapes your brain's capacity for integration."""
        },
        {
            "id": 4,
            "title": "Lesson 4: Navigating Difficult Emotions",
            "content": """What do we do when integration feels impossible? When emotions overwhelm thinking, or thinking suppresses feeling?

Working with intensity:
• Window of tolerance concept
• Grounding techniques for overwhelm
• Cognitive reframing without spiritual bypassing
• When to seek additional support

You don't have to choose between heart and mind. You're learning to honor both."""
        },
        {
            "id": 5,
            "title": "Lesson 5: Living Integrated",
            "content": """The final lesson is really the beginning—taking these practices into daily life.

Creating sustainable integration:
• Morning and evening integration rituals
• Applying heart-mind wisdom to relationships
• Decision-making from your integrated center
• Recognizing when you've fallen out of balance
• Building a lifelong practice

You are neither just your thoughts nor just your feelings. You are the conscious space in which both arise. That awareness changes everything."""
        },
    ],
    4: [  # Course 4: Navigating Grief with Grace
        {
            "id": 1,
            "title": "Lesson 1: Welcome to the Wilderness",
            "content": """Grief is not a problem to solve. It's a sacred, messy, necessary wilderness to walk through.

Beginning with compassion:
• What grief is (and what it isn't)
• The many faces of loss beyond death
• Why the "stages" of grief are actually more like waves
• Permission to grieve in your own way and time

You are not broken. You are grieving. And that is profoundly human."""
        },
        {
            "id": 2,
            "title": "Lesson 2: The Waves of Grief",
            "content": """Some days the ocean is calm. Other days, a wave knocks you off your feet without warning.

Understanding grief's rhythm:
• Why grief comes in waves, not stages
• Triggers and anniversaries
• Physical manifestations of grief
• Creating space for the unexpected

The waves will keep coming—but gradually, you'll learn to swim."""
        },
        {
            "id": 3,
            "title": "Lesson 3: What Grief Needs",
            "content": """Grief needs witnessing, not fixing. It needs presence, not advice. It needs time, not timelines.

Essential grief tending:
• Creating rituals to honor what was lost
• Journaling prompts for expression
• The importance of rest and gentleness
• Asking for and accepting support

Your grief is a testament to your love. Honor it accordingly."""
        },
        {
            "id": 4,
            "title": "Lesson 4: Complicated Grief",
            "content": """Sometimes grief is compounded by complexity—ambivalent relationships, traumatic loss, disenfranchised grief that others don't recognize.

Working with complications:
• When grief gets stuck or prolonged
• Processing mixed emotions (relief and sadness can coexist)
• Grieving what never was
• When professional support is needed

All grief is valid. All loss deserves to be mourned."""
        },
        {
            "id": 5,
            "title": "Lesson 5: Grief and Guilt",
            "content": """Guilt is grief's shadow companion. 'What if' and 'if only' haunt the grieving heart.

Untangling guilt:
• The difference between guilt and regret
• Forgiving yourself for being human
• Making meaning without making it your fault
• Releasing what you cannot change

You did the best you could with what you knew. That is enough."""
        },
        {
            "id": 6,
            "title": "Lesson 6: Finding Meaning",
            "content": """We don't "get over" grief. We learn to carry it differently. Some losses change us forever—and that's okay.

Integration and meaning:
• Post-traumatic growth after loss
• How grief can deepen compassion
• Honoring the past while choosing the future
• Continuing bonds in healthy ways

You will laugh again. You will find joy again. And you will always love what you lost. These truths can coexist."""
        },
        {
            "id": 7,
            "title": "Lesson 7: Living While Grieving",
            "content": """Life doesn't pause for grief. This lesson is about integration—allowing grief and growth to occupy the same space.

Moving forward, not on:
• Re-engaging with life without guilt
• Building new routines and rituals
• When grief resurfaces (and it will)
• Finding your new normal

Grief is love with nowhere to go. You're learning to let it flow through you rather than drown in it."""
        },
        {
            "id": 8,
            "title": "Lesson 8: Grace for the Journey",
            "content": """Our final lesson returns to the title: grace. Not the absence of struggle, but compassion within it.

Closing with wholeness:
• Reflecting on your journey through this course
• Tools for future waves of grief
• Building your ongoing support system
• A letter to your future self
• Celebrating your courage

You showed up for yourself in the hardest of times. That is grace. That is strength. That is healing.

May you walk forward with tender resilience."""
        },
    ],
}

@lessons_bp.route("/<int:course_id>/<int:lesson_id>")
@login_required
def show_lesson(course_id, lesson_id):
    """Display a specific lesson for a course"""
    # Check if user has purchased this course (check both Purchase and Enrollment tables)
    purchase = Purchase.query.filter_by(
        user_id=current_user.id,
        module_id=course_id,
        payment_status='completed'
    ).first()
    
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        module_id=course_id
    ).first()
    
    if not purchase and not enrollment:
        return redirect(url_for('courses.course_detail', course_id=course_id))
    
    # Get lessons for this course
    lessons = lesson_data.get(course_id, [])
    lesson = next((l for l in lessons if l["id"] == lesson_id), None)
    
    if not lesson:
        return render_template("lessons/lesson_complete.html", course_id=course_id)
    
    # Determine navigation
    next_id = lesson_id + 1 if any(l["id"] == lesson_id + 1 for l in lessons) else None
    prev_id = lesson_id - 1 if any(l["id"] == lesson_id - 1 for l in lessons) else None
    
    total_lessons = len(lessons)
    
    return render_template(
        "lessons/lesson.html",
        course_id=course_id,
        lesson=lesson,
        next_id=next_id,
        prev_id=prev_id,
        total_lessons=total_lessons,
        current_lesson_num=lesson_id
    )

@lessons_bp.route("/<int:course_id>/complete")
@login_required
def course_complete(course_id):
    """Show completion page after all lessons are done"""
    return render_template("lessons/lesson_complete.html", course_id=course_id)
