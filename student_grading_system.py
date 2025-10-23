# OOP WITH PYTHON ASSIGNMENT 3

# *** QUESTION 4 ***
print("\n\n*** QUESTION 4 ***\n\n")


import json
from abc import ABC, abstractmethod


class Student(ABC):
    def __init__(self, student_id, name, marks):
        if not isinstance(marks, dict) or not all(isinstance(v, (int, float)) for v in marks.values()):
            raise ValueError("Marks must be a dictionary with numeric values.")
        self.student_id = student_id
        self.name = name
        self.marks = marks

    def compute_total(self):
        return sum(self.marks.values())

    def compute_average(self):
        return self.compute_total() / len(self.marks) if self.marks else 0

    def get_grade(self):
        avg = self.compute_average()
        if avg >= 80:
            return 'A'
        elif avg >= 70:
            return 'B'
        elif avg >= 60:
            return 'C'
        elif avg >= 50:
            return 'D'
        else:
            return 'F'

    def evaluate(self):
        
    #    Polymorphic method: returns coursework evaluation string.
        
        return f"{self.name} (ID: {self.student_id}) - Grade: {self.get_grade()}"

    def to_dict(self):
        return {
            "type": "Student",
            "student_id": self.student_id,
            "name": self.name,
            "marks": self.marks
        }

    @staticmethod
    def from_dict(data):
        if data["type"] == "PostgraduateStudent":
            return PostgraduateStudent(
                student_id=data["student_id"],
                name=data["name"],
                marks=data["marks"],
                research_topic=data["research_topic"]
            )
        else:
            return UndergraduateStudent(
                student_id=data["student_id"],
                name=data["name"],
                marks=data["marks"]
            )


class UndergraduateStudent(Student):
    pass  # No extra functionality for now


class PostgraduateStudent(Student):
    def __init__(self, student_id, name, marks, research_topic):
        super().__init__(student_id, name, marks)
        self.research_topic = research_topic

    def evaluate_thesis(self):
        
   #     Dummy evaluation logic: pass if average >= 60
        
        return "Pass" if self.compute_average() >= 60 else "Revise"

    def evaluate(self):
        
   #     Overridden polymorphic method: includes thesis result.
        
        grade = self.get_grade()
        thesis_result = self.evaluate_thesis()
        return (f"{self.name} (ID: {self.student_id}) - Grade: {grade}, "
                f"Thesis: {thesis_result} [{self.research_topic}]")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "PostgraduateStudent"
        data["research_topic"] = self.research_topic
        return data


# *** JSON Utility Functions ***

def save_students_to_json(students, filename="students.json"):
    try:
        with open(filename, "w") as f:
            json.dump([s.to_dict() for s in students], f, indent=4)
        print(f"Saved {len(students)} students to '{filename}'")
    except Exception as e:
        print(f"Error saving data: {e}")


def load_students_from_json(filename="students.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [Student.from_dict(item) for item in data]
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


# *** Demonstration ***
if __name__ == "__main__":
    students = [
        UndergraduateStudent("UG001", "Samuel", {"Math": 78, "English": 85, "ICT": 70}),
        PostgraduateStudent("PG001", "Mariam", {"Research": 82, "Ethics": 75}, "AI in Smart City"),
        PostgraduateStudent("PG002", "Emilly", {"Research": 55, "Seminar": 60}, "Data Science Models"),
    ]

    print("*** Student Evaluations ***")
    for s in students:
        print(s.evaluate())

    # Save to JSON
    save_students_to_json(students)

    print("\n*** Reloaded from JSON ***")
    reloaded = load_students_from_json()
    for s in reloaded:
        print(s.evaluate())
