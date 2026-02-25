from datetime import datetime, timedelta

def get_student_stats_pipeline(department, college_name, today_str):
    """
    Aggregation pipeline to get student statistics for a department
    """
    return [
        # 1. Match students in the specific department and college
        {
            "$match": {
                "role": "student",
                "department": department,
                "college_name": college_name
            }
        },
        # 2. Lookup existing profile for attendance percentage
        {
            "$lookup": {
                "from": "student_profiles",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "profile"
            }
        },
        # 3. Aggressive Deduplication: Project only the first profile if multiple exist
        {
            "$project": {
                "role": 1,
                "department": 1,
                "college_name": 1,
                "profile": {"$arrayElemAt": ["$profile", 0]}
            }
        },
        # 4. Lookup attendance for ONE specific day (Today)
        {
            "$lookup": {
                "from": "attendance",
                "let": {"student_id": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$student_id", "$$student_id"]},
                                    {"$eq": ["$date", today_str]}
                                ]
                            }
                        }
                    },
                    {"$limit": 1} # Ensure only 1 attendance record per day counts
                ],
                "as": "today_attendance"
            }
        },
        {
            "$unwind": {
                "path": "$today_attendance",
                "preserveNullAndEmptyArrays": True
            }
        },
        # 5. Group to calculate counts
        {
            "$group": {
                "_id": None,
                "total_students": {"$sum": 1},
                "present_today": {
                    "$sum": {
                        "$cond": [{"$eq": ["$today_attendance.status", "present"]}, 1, 0]
                    }
                },
                "absent_today": {
                    "$sum": {
                        "$cond": [{"$eq": ["$today_attendance.status", "absent"]}, 1, 0]
                    }
                },
                "total_attendance_percentage": {
                    "$sum": {"$ifNull": ["$profile.attendance_percentage", 0]}
                },
                "students_below_75": {
                    "$sum": {
                        "$cond": [
                            {"$lt": [{"$ifNull": ["$profile.attendance_percentage", 0]}, 75]}, 
                            1, 
                            0
                        ]
                    }
                }
            }
        },
        # 6. Format the output
        {
            "$project": {
                "_id": 0,
                "total": "$total_students",
                "present_today": "$present_today",
                "absent_today": "$absent_today",
                "below_75": "$students_below_75",
                # Avoid division by zero
                "average_attendance": {
                    "$cond": [
                        {"$gt": ["$total_students", 0]},
                        {"$round": [{"$divide": ["$total_attendance_percentage", "$total_students"]}, 2]},
                        0
                    ]
                }
            }
        }
    ]

def get_learning_levels_pipeline(department, college_name):
    """
    Aggregation pipeline to categorize students by learning levels based on average marks
    """
    return [
        # 1. Match students
        {
            "$match": {
                "role": "student",
                "department": department,
                "college_name": college_name
            }
        },
        # 2. Join with profiles to get marks
        {
            "$lookup": {
                "from": "student_profiles",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "profile"
            }
        },
        # Fix: Project only the first profile to avoid duplication
        {
            "$project": {
                "profile": {"$arrayElemAt": ["$profile", 0]}
            }
        },
        {
            "$project": {
                "avg_marks": {
                    "$avg": [
                        "$profile.sem_1_marks", "$profile.sem_2_marks", 
                        "$profile.sem_3_marks", "$profile.sem_4_marks",
                        "$profile.sem_5_marks", "$profile.sem_6_marks", 
                        "$profile.sem_7_marks", "$profile.sem_8_marks"
                    ]
                }
            }
        },
        # 4. Categorize based on average
        {
            "$project": {
                "category": {
                    "$switch": {
                        "branches": [
                            # < 40: Slow
                            {"case": {"$lt": ["$avg_marks", 40]}, "then": "slow"},
                            # 40-70: Intermediate
                            {"case": {"$and": [{"$gte": ["$avg_marks", 40]}, {"$lte": ["$avg_marks", 70]}]}, "then": "intermediate"},
                            # > 70: Advanced (71+)
                            {"case": {"$gt": ["$avg_marks", 70]}, "then": "advanced"}
                        ],
                        "default": "ongoing" # If no marks
                    }
                }
            }
        },
        # 5. Group by category and count
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1}
            }
        }
    ]
