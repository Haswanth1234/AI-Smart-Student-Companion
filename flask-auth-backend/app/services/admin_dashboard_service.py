from datetime import datetime, timedelta
from bson import ObjectId
from app import get_db
from app.aggregations.admin_dashboard import get_student_stats_pipeline, get_learning_levels_pipeline

class AdminDashboardService:
    def __init__(self):
        self.db = get_db()
        self.users = self.db['users']
        self.alerts = self.db['alerts']
        self.tasks = self.db['tasks']
        
    def get_overview(self, department, college_name):
        """
        Get comprehensive dashboard overview for admin
        """
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # 1. Get Student Statistics (Total, Attendance)
        student_stats_pipeline = get_student_stats_pipeline(department, college_name, today_str)
        student_stats_result = list(self.users.aggregate(student_stats_pipeline))
        
        # Default stats if no students found
        default_stats = {
            "total": 0, "present_today": 0, "absent_today": 0, 
            "average_attendance": 0, "below_75": 0
        }
        
        students_data = student_stats_result[0] if student_stats_result else default_stats
        
        # 2. Get Learning Levels
        learning_pipeline = get_learning_levels_pipeline(department, college_name)
        learning_results = list(self.users.aggregate(learning_pipeline))
        
        learning_levels = {"slow": 0, "intermediate": 0, "advanced": 0}
        for item in learning_results:
            if item['_id'] in learning_levels:
                learning_levels[item['_id']] = item['count']
                
        # 3. Get Alerts Summary
        # Note: Assuming alerts collection has 'type', 'department', 'college_name' or linked to student
        # For simplicity, we count by type for students in this dept
        # This might need a join if alerts don't have dept directly, but let's assume they might
        # Or we query alerts linked to students of this dept. 
        # Better approach: Aggregate alerts by looking up student details
        
        # 3. Get Alerts Summary & Recent Alerts
        alerts_pipeline = [
            {
                "$set": {
                    "student_id_obj": { "$toObjectId": "$student_id" }
                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "student_id_obj",
                    "foreignField": "_id",
                    "as": "student"
                }
            },
            {"$unwind": "$student"},
            {
                "$match": {
                    "student.department": department,
                    "student.college_name": college_name,
                }
            },
            {
                "$facet": {
                    "summary": [
                        {
                            "$group": {
                                "_id": "$type",
                                "count": {"$sum": 1}
                            }
                        }
                    ],
                    "recent": [
                        {"$sort": {"created_at": -1}},
                        {"$limit": 5},
                        {
                            "$project": {
                                "_id": {"$toString": "$_id"},
                                "type": 1,
                                "message": 1,
                                "severity": 1,
                                "created_at": 1,
                                "student_name": "$student.name",
                                "student_id": {"$toString": "$student._id"}
                            }
                        }
                    ]
                }
            }
        ]
        
        alerts_agg = list(self.db['student_alerts'].aggregate(alerts_pipeline))[0]
        alerts_results = alerts_agg['summary']
        recent_alerts = alerts_agg['recent']
        
        alerts_data = {"total": 0, "attendance": 0, "performance": 0}
        for item in alerts_results:
            alerts_data["total"] += item['count']
            if "attendance" in str(item.get('_id', '')).lower():
                alerts_data["attendance"] += item['count']
            elif "performance" in str(item.get('_id', '')).lower() or "academic" in str(item.get('_id', '')).lower():
                alerts_data["performance"] += item['count']
                
        # 4. Get Tasks Summary & Recent Tasks
        tasks_pipeline = [
             {
                "$set": {
                    "student_id_obj": { "$toObjectId": "$user_id" }
                }
            },
             {
                "$lookup": {
                    "from": "users",
                    "localField": "student_id_obj",
                    "foreignField": "_id",
                    "as": "student"
                }
            },
            {"$unwind": "$student"},
            {
                "$match": {
                    "student.department": department,
                    "student.college_name": college_name
                }
            },
            {
                "$facet": {
                    "summary": [
                        {
                            "$group": {
                                "_id": "$status",
                                "count": {"$sum": 1}
                            }
                        }
                    ],
                    "recent": [
                        {"$match": {"status": "pending"}},
                        {"$sort": {"due_date": 1}},
                        {"$limit": 5},
                        {
                            "$project": {
                                "_id": {"$toString": "$_id"},
                                "title": 1,
                                "priority": 1,
                                "due_date": 1,
                                "student_name": "$student.name",
                                "student_id": {"$toString": "$student._id"}
                            }
                        }
                    ]
                }
            }
        ]
        
        tasks_agg = list(self.tasks.aggregate(tasks_pipeline))[0]
        tasks_results = tasks_agg['summary']
        recent_tasks = tasks_agg['recent']
        
        tasks_data = {"total": 0, "pending": 0, "completed": 0}
        for item in tasks_results:
            count = item['count']
            tasks_data["total"] += count
            status = str(item.get('_id', '')).lower()
            if status == 'pending':
                tasks_data["pending"] += count
            elif status == 'completed':
                tasks_data["completed"] += count
        
        # 5. Format timestamps for JSON
        for alert in recent_alerts:
            if isinstance(alert.get('created_at'), datetime):
                alert['created_at'] = alert['created_at'].isoformat()
        for task in recent_tasks:
            if isinstance(task.get('due_date'), datetime):
                task['due_date'] = task['due_date'].isoformat()
        
        return {
            "department": department,
            "college_name": college_name,
            "students": students_data,
            "learning_levels": learning_levels,
            "alerts": {**alerts_data, "recent": recent_alerts},
            "tasks": {**tasks_data, "recent": recent_tasks}
        }

    def get_attendance_summary(self, admin_id):
        """
        Get specific attendance summary for Admin Attendance Page
        """
        # 1. Get Admin Details
        admin = self.users.find_one({"_id": ObjectId(admin_id)})
        if not admin:
            raise ValueError("Admin not found")
        
        department = admin.get('department')
        college_name = admin.get('college_name')
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # 2. Reuse efficient pipeline from overview
        student_stats_pipeline = get_student_stats_pipeline(department, college_name, today_str)
        student_stats_result = list(self.users.aggregate(student_stats_pipeline))
        
        default_stats = {
            "total_students": 0, "present_today": 0, "absent_today": 0, 
            "average_attendance": 0, "students_below_75": 0
        }
        
        # Mapping aggregation result keys to expected output keys
        # Aggregation returns: total, present_today, absent_today, below_75, average_attendance
        agg_data = student_stats_result[0] if student_stats_result else {}
        
        summary = {
            "total_students": agg_data.get('total', 0),
            "present_today": agg_data.get('present_today', 0),
            "absent_today": agg_data.get('absent_today', 0),
            "average_attendance": agg_data.get('average_attendance', 0),
            "students_below_75": agg_data.get('below_75', 0)
        }
        
        # 3. Get List of Defaulters (< 75%)
        # We need a separate query/pipeline for the detailed list
        defaulters_pipeline = [
            {
                "$match": {
                    "role": "student",
                    "department": department,
                    "college_name": college_name
                }
            },
            {
                "$lookup": {
                    "from": "student_profiles",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "profile"
                }
            },
            {
                "$project": {
                    "name": 1,
                    "roll_number": 1,
                    "profile": {"$arrayElemAt": ["$profile", 0]}
                }
            },
            {
                "$project": {
                    "name": 1,
                    "roll_number": 1,
                    "attendance_percentage": {"$ifNull": ["$profile.attendance_percentage", 0]}
                }
            },
            {
                "$match": {
                    "attendance_percentage": {"$lt": 75}
                }
            },
            {"$sort": {"attendance_percentage": 1}}
        ]
        
        defaulters = list(self.users.aggregate(defaulters_pipeline))
        
        # Format defaulters
        formatted_defaulters = []
        for d in defaulters:
            formatted_defaulters.append({
                "id": str(d['_id']),
                "name": d.get('name'),
                "roll_number": d.get('roll_number', 'N/A'),
                "attendance_percentage": d.get('attendance_percentage')
            })
            
        return {
            "department": department,
            "college_name": college_name,
            "summary": summary,
            "defaulters": formatted_defaulters
        }

    def get_student_tasks(self, department, college_name):
        """
        Get all tasks for students in the department
        """
        pipeline = [
            # 1. Join tasks with users (students)
            {
                "$set": {
                    "student_id_obj": { "$toObjectId": "$user_id" }
                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "student_id_obj",
                    "foreignField": "_id",
                    "as": "student"
                }
            },
            {"$unwind": "$student"},
            # 2. Filter by Admin's Dept/College
            {
                "$match": {
                    "student.department": department,
                    "student.college_name": college_name,
                    "student.role": "student"
                }
            },
            # 3. Project relevant fields
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "title": 1,
                    "description": 1,
                    "status": 1,
                    "priority": 1,
                    "due_date": 1,
                    "created_at": 1,
                    "student_name": "$student.name",
                    "student_roll": "$student.roll_number",
                    "student_id": {"$toString": "$student._id"}
                }
            },
            # 4. Sort by due date (soonest first)
            {"$sort": {"due_date": 1}}
        ]
        
        tasks = list(self.tasks.aggregate(pipeline))
        return tasks

    def get_all_student_alerts(self, department, college_name):
        """
        Get all alerts for students in the department
        """
        pipeline = [
            # 1. Join alerts with users (students)
            {
                "$set": {
                    "student_id_obj": { "$toObjectId": "$student_id" }
                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "student_id_obj",
                    "foreignField": "_id",
                    "as": "student"
                }
            },
            {"$unwind": "$student"},
            # 2. Filter by Admin's Dept/College
            {
                "$match": {
                    "student.department": department,
                    "student.college_name": college_name,
                    "student.role": "student"
                }
            },
            # 3. Project relevant fields
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "type": 1, 
                    "alert_type": 1, # specific type
                    "title": 1,
                    "message": 1,
                    "severity": 1,
                    "is_read": 1,
                    "created_at": 1,
                    "student_name": "$student.name",
                    "student_roll": "$student.roll_number",
                    "student_id": {"$toString": "$student._id"}
                }
            },
            # 4. Sort by date (newest first)
            {"$sort": {"created_at": -1}}
        ]
        
        # Note: Using self.alerts collection which seems to be the one admin service uses
        # But per analysis, there is also 'student_alerts' collection.
        # Assuming we need to query 'student_alerts' actually.
        # Let's switch to checking 'student_alerts' collection to be safe,
        # or stick to self.alerts if it was initialized correctly.
        # Initialize it just in case:
        student_alerts_collection = self.db['student_alerts']
        
        alerts = list(student_alerts_collection.aggregate(pipeline))
        
        # Format date for frontend consistency if needed, or leave as ISODate
        for alert in alerts:
            if 'created_at' in alert and isinstance(alert['created_at'], datetime):
                 alert['created_at'] = alert['created_at'].isoformat()
                 
        return alerts

    def resolve_alert(self, alert_id, resolution_notes, admin_id):
        """
        Mark a student alert as resolved
        """
        student_alerts_collection = self.db['student_alerts']
        
        # Check if alert exists
        alert = student_alerts_collection.find_one({"_id": ObjectId(alert_id)})
        if not alert:
            raise ValueError("Alert not found")
            
        # Update alert
        result = student_alerts_collection.update_one(
            {"_id": ObjectId(alert_id)},
            {
                "$set": {
                    "status": "resolved",
                    "resolution_notes": resolution_notes,
                    "resolved_by": ObjectId(admin_id),
                    "resolved_at": datetime.now()
                }
            }
        )
        
        return result.modified_count > 0

    def create_task(self, task_data, admin_id):
        """
        Create a new task for a student
        """
        # Validate student exists
        student = self.users.find_one({"_id": ObjectId(task_data['student_id']), "role": "student"})
        if not student:
            raise ValueError("Student not found")

        new_task = {
            "title": task_data['title'],
            "description": task_data.get('description', ''),
            "user_id": ObjectId(task_data['student_id']),
            "assigned_by": ObjectId(admin_id),
            "priority": task_data.get('priority', 'medium'), # low, medium, high
            "due_date": datetime.fromisoformat(task_data['due_date'].replace('Z', '+00:00')) if isinstance(task_data['due_date'], str) else task_data['due_date'],
            "status": "pending",
            "created_at": datetime.now()
        }
        
        result = self.tasks.insert_one(new_task)
        return str(result.inserted_id)

    def update_task(self, task_id, task_data):
        """
        Update an existing task
        """
        update_fields = {}
        
        if 'title' in task_data:
            update_fields['title'] = task_data['title']
        if 'description' in task_data:
            update_fields['description'] = task_data['description']
        if 'priority' in task_data:
            update_fields['priority'] = task_data['priority']
        if 'due_date' in task_data:
             update_fields['due_date'] = datetime.fromisoformat(task_data['due_date'].replace('Z', '+00:00')) if isinstance(task_data['due_date'], str) else task_data['due_date']
        if 'status' in task_data:
            update_fields['status'] = task_data['status']
            
        if not update_fields:
            return False
            
        result = self.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_fields}
        )
        
        return result.modified_count > 0

    def delete_task(self, task_id):
        """
        Delete a task
        """
        result = self.tasks.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0

    def get_reports_data(self, department, college_name):
        """
        Get aggregated data for reports
        """
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # 1. Attendance Trends (Last 7 Days)
        # We need a proper aggregation for this. For now, let's mock realistic data based on actual attendance if possible,
        # or just query the last 7 distinct dates from attendance collection.
        
        # Mocking 7-day trend for UI visualization purposes, as real historical data might be sparse in dev
        # In production, this would be an aggregation over 'attendance' collection grouped by date
        # Ideally: match department students -> lookup attendance -> group by date -> avg status
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)
        
        attendance_trend = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            # In a real scenario, query DB for this date's average. 
            # For this prototype/dev, we'll return the structure and maybe some real data if available for today
            
            day_stats = {
                "date": current_date.strftime('%a'), # Mon, Tue
                "full_date": date_str,
                "present": 0,
                "absent": 0
            }
            
            if date_str == today_str:
                # Use real data for today
                stats = self.get_overview(department, college_name)
                # Parse "85%" -> 85
                day_stats["present"] = stats['students']['present_today']
                day_stats["absent"] = stats['students']['absent_today']
            else:
                # Random/Mock for other days to show chart capability if no real data
                # Or leave 0 if we want strict accuracy. Let's leave 0 to avoid fake data unless requested.
                # Actually, better to have 0 than fake data for "Reports".
                pass
                
            attendance_trend.append(day_stats)
            current_date += timedelta(days=1)
            
        # 2. Performance Distribution (Learning Levels)
        # Reuse existing pipeline
        learning_pipeline = get_learning_levels_pipeline(department, college_name)
        learning_results = list(self.users.aggregate(learning_pipeline))
        
        performance_dist = [
            {"name": "Advanced (>70%)", "value": 0, "color": "#10b981"},  # emerald-500
            {"name": "Intermediate (40-70%)", "value": 0, "color": "#f59e0b"}, # amber-500
            {"name": "Needs Improvement (<40%)", "value": 0, "color": "#ef4444"} # red-500
        ]
        
        for item in learning_results:
            cat = item['_id']
            count = item['count']
            if cat == 'advanced':
                performance_dist[0]["value"] = count
            elif cat == 'intermediate':
                performance_dist[1]["value"] = count
            elif cat == 'slow':
                performance_dist[2]["value"] = count
                
        # 3. Top Performers (Top 5 by avg marks)
        top_performers_pipeline = [
            {
                "$match": {
                    "role": "student",
                    "department": department,
                    "college_name": college_name
                }
            },
            {
                "$lookup": {
                    "from": "student_profiles",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "profile"
                }
            },
            {"$unwind": "$profile"}, # Only students with profiles
            {
                "$project": {
                    "name": 1,
                    "roll_number": 1,
                    "avg_marks": {
                        "$avg": [
                            "$profile.sem_1_marks", "$profile.sem_2_marks", 
                            "$profile.sem_3_marks", "$profile.sem_4_marks",
                            "$profile.sem_5_marks", "$profile.sem_6_marks", 
                            "$profile.sem_7_marks", "$profile.sem_8_marks"
                        ]
                    },
                    "attendance": "$profile.attendance_percentage"
                }
            },
            {"$sort": {"avg_marks": -1}},
            {"$limit": 5}
        ]
        
        top_performers = list(self.users.aggregate(top_performers_pipeline))
        for s in top_performers:
            s['_id'] = str(s['_id'])
            s['avg_marks'] = round(s.get('avg_marks') or 0, 1)
            
        # 4. At-Risk Students (Low Attendance < 75%)
        at_risk_pipeline = [
             {
                "$match": {
                    "role": "student",
                    "department": department,
                    "college_name": college_name
                }
            },
            {
                "$lookup": {
                    "from": "student_profiles",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "profile"
                }
            },
            {"$unwind": "$profile"},
            {
                "$match": {
                    "profile.attendance_percentage": {"$lt": 75}
                }
            },
             {
                "$project": {
                    "name": 1,
                    "roll_number": 1,
                    "attendance": "$profile.attendance_percentage",
                    "email": 1
                }
            },
            {"$sort": {"attendance": 1}},
            {"$limit": 10} # Top 10 most critical
        ]
        
        at_risk_students = list(self.users.aggregate(at_risk_pipeline))
        for s in at_risk_students:
            s['_id'] = str(s['_id'])

        return {
            "attendance_trend": attendance_trend,
            "performance_distribution": performance_dist,
            "top_performers": top_performers,
            "at_risk_students": at_risk_students
        }