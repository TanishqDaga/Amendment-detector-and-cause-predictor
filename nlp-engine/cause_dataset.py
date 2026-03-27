import random
import json

SECTORS = [
    "Attendance",
    "Evaluation",
    "Fees",
    "Registration",
    "Discipline",
    "Internship",
    "Scholarship"
]

CAUSE_BANK = {
    "Attendance Increase": [
        "due to poor student attendance trends, low classroom engagement, and the need to improve academic discipline",
        "to ensure consistent participation, improve learning outcomes, and satisfy accreditation requirements",
        "to reduce absenteeism and ensure students meet minimum academic engagement standards"
    ],

    "Evaluation Change": [
        "to improve assessment fairness, reduce over-dependence on final exams, and promote continuous learning",
        "to align evaluation with modern education practices and industry expectations",
        "to better measure student performance across multiple dimensions like assignments and projects"
    ],

    "Fee Change": [
        "to ensure financial sustainability, manage institutional costs, and support infrastructure development",
        "to discourage late payments and ensure timely fee collection",
        "to compensate for administrative overhead and operational expenses"
    ],

    "Registration Change": [
        "to provide flexibility for students while maintaining administrative control over course allocation",
        "to allow defaulters to complete registration while enforcing penalties for delays",
        "to handle high student volume and system constraints efficiently"
    ],

    "Discipline Change": [
        "to enforce stricter behavioral policies and maintain campus integrity",
        "to deter misconduct and ensure a safe academic environment",
        "to strengthen institutional discipline and accountability mechanisms"
    ],

    "Internship Change": [
        "to improve practical exposure and industry readiness of students",
        "to align curriculum with industry expectations and employability standards",
        "to enhance hands-on experience and skill development"
    ]
}


RULE_TEMPLATES = {
    "Attendance Increase": (
        "Students must maintain at least {old}% attendance",
        "Students must maintain at least {new}% attendance"
    ),
    "Evaluation Change": (
        "CAT weightage is {old}%",
        "CAT weightage is {new}% with assignments included"
    ),
    "Fee Change": (
        "Students must pay fees before deadline",
        "Students must pay fees before deadline with late fee ₹{new}"
    ),
    "Internship Change": (
        "internship of {old} weeks",
        "internship of {new} weeks"
    )
}


def generate_sample():
    change_type = random.choice(list(RULE_TEMPLATES.keys()))
    cause = random.choice(CAUSE_BANK[change_type])

    old_val = random.randint(50, 80)
    new_val = old_val + random.randint(5, 20)

    old_rule = RULE_TEMPLATES[change_type][0].format(old=old_val)
    new_rule = RULE_TEMPLATES[change_type][1].format(new=new_val)

    return {
        "old": old_rule,
        "new": new_rule,
        "label": cause
    }


def generate_dataset(size=50000):
    dataset = [generate_sample() for _ in range(size)]

    with open("cause_dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)

    print(f"✅ Massive dataset generated: {size} samples")


if __name__ == "__main__":
    generate_dataset(50000)