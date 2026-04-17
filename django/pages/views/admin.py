from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    # Bu yerda siz statistik ma’lumotlarni jo‘natasiz
    stats = {
        'students': 120,
        'courses': 25,
        'teachers': 10,
        'active_users': 45,
    }
    return render(request, 'admin/dashboard.html', {'courses': stats})


# views.py da courses konteksti
@login_required
def courses_view(request):
    courses_data = [
        {
            'title': 'Python Asoslari',
            'instructor': 'Ali Valiyev',
            'description': 'Python dasturlash tilini noldan o\'rganing. Asosiy tushunchalar, ma\'lumotlar tuzilmasi va loyihalar.',
            'students': 145,
            'lessons': 24,
            'duration': 8,
            'progress': 85,
            'rating': 4.8,
            'reviews': 89,
            'color': 'primary',
            'status': 'Aktiv',
            'status_color': 'success'
        },
        {
            'title': 'Web Dasturlash',
            'instructor': 'Sevara Xolmirzayeva',
            'description': 'HTML, CSS, JavaScript va React asoslarini o\'rganib, zamonaviy web ilovalar yarating.',
            'students': 203,
            'lessons': 36,
            'duration': 12,
            'progress': 72,
            'rating': 4.9,
            'reviews': 124,
            'color': 'success',
            'status': 'Aktiv',
            'status_color': 'success'
        },
        {
            'title': 'Data Science',
            'instructor': 'Javohir Tursunov',
            'description': 'Ma\'lumotlar tahlili, machine learning va vizualizatsiya asoslarini o\'rganing.',
            'students': 98,
            'lessons': 30,
            'duration': 10,
            'progress': 63,
            'rating': 4.7,
            'reviews': 67,
            'color': 'warning',
            'status': 'Aktiv',
            'status_color': 'success'
        },
        {
            'title': 'Mobile Development',
            'instructor': 'Azizbek Rahimov',
            'description': 'React Native yordamida iOS va Android platformalari uchun mobil ilovalar yarating.',
            'students': 76,
            'lessons': 28,
            'duration': 9,
            'progress': 45,
            'rating': 4.6,
            'reviews': 45,
            'color': 'info',
            'status': 'Yangi',
            'status_color': 'primary'
        },
        {
            'title': 'UI/UX Dizayn',
            'instructor': 'Dilnoza Xasanova',
            'description': 'Figma yordamida zamonaviy interfeyslar dizayn qilishni o\'rganing.',
            'students': 112,
            'lessons': 20,
            'duration': 6,
            'progress': 92,
            'rating': 4.8,
            'reviews': 78,
            'color': 'danger',
            'status': 'Yakunlangan',
            'status_color': 'secondary'
        },
        {
            'title': 'Backend Development',
            'instructor': 'Shoxrux Abdurahmonov',
            'description': 'Django va Node.js asoslarini o\'rganib, kuchli backend tizimlar yarating.',
            'students': 134,
            'lessons': 32,
            'duration': 11,
            'progress': 78,
            'rating': 4.7,
            'reviews': 92,
            'color': 'primary',
            'status': 'Aktiv',
            'status_color': 'success'
        }
    ]
    
    return render(request, 'admin/contents/courses.html', {'courses': courses_data})

# views.py da teachers konteksti
@login_required
def teachers_view(request):
    teachers_data = [
        {
            'name': 'Ali Valiyev',
            'initials': 'AV',
            'email': 'ali.valiyev@itacademy.uz',
            'specialization': 'Python Dasturlash',
            'courses': 4,
            'students': 320,
            'experience': 5,
            'rating': 4.8,
            'reviews': 145,
            'skills': ['Python', 'Django', 'Flask', 'PostgreSQL'],
            'status': 'Aktiv',
            'status_color': 'success',
            'color': 'primary'
        },
        {
            'name': 'Sevara Xolmirzayeva',
            'initials': 'SX',
            'email': 'sevara.x@itacademy.uz',
            'specialization': 'Web Dasturlash',
            'courses': 3,
            'students': 280,
            'experience': 4,
            'rating': 4.9,
            'reviews': 167,
            'skills': ['JavaScript', 'React', 'Node.js', 'MongoDB'],
            'status': 'Aktiv',
            'status_color': 'success',
            'color': 'success'
        },
        {
            'name': 'Javohir Tursunov',
            'initials': 'JT',
            'email': 'javohir.t@itacademy.uz',
            'specialization': 'Data Science',
            'courses': 2,
            'students': 150,
            'experience': 6,
            'rating': 4.7,
            'reviews': 89,
            'skills': ['Python', 'Pandas', 'ML', 'SQL'],
            'status': 'Aktiv',
            'status_color': 'success',
            'color': 'warning'
        },
        {
            'name': 'Dilnoza Xasanova',
            'initials': 'DX',
            'email': 'dilnoza.x@itacademy.uz',
            'specialization': 'UI/UX Dizayn',
            'courses': 3,
            'students': 180,
            'experience': 3,
            'rating': 4.6,
            'reviews': 76,
            'skills': ['Figma', 'Adobe XD', 'Photoshop', 'Illustrator'],
            'status': 'Dam olmoqda',
            'status_color': 'warning',
            'color': 'danger'
        },
        {
            'name': 'Azizbek Rahimov',
            'initials': 'AR',
            'email': 'azizbek.r@itacademy.uz',
            'specialization': 'Mobile Development',
            'courses': 2,
            'students': 120,
            'experience': 4,
            'rating': 4.5,
            'reviews': 67,
            'skills': ['React Native', 'Flutter', 'Firebase', 'REST API'],
            'status': 'Aktiv',
            'status_color': 'success',
            'color': 'info'
        },
        {
            'name': 'Shoxrux Abdurahmonov',
            'initials': 'SA',
            'email': 'shoxrux.a@itacademy.uz',
            'specialization': 'Backend Development',
            'courses': 3,
            'students': 210,
            'experience': 5,
            'rating': 4.7,
            'reviews': 98,
            'skills': ['Node.js', 'Express', 'MongoDB', 'Docker'],
            'status': 'Faol emas',
            'status_color': 'secondary',
            'color': 'primary'
        }
    ]
    
    # Calculate statistics
    active_teachers = len([t for t in teachers_data if t['status'] == 'Aktiv'])
    active_percentage = round((active_teachers / len(teachers_data)) * 100)
    average_rating = round(sum(t['rating'] for t in teachers_data) / len(teachers_data), 1)
    total_courses = sum(t['courses'] for t in teachers_data)
    
    context = {
        'teachers': teachers_data,
        'active_teachers': active_teachers,
        'active_percentage': active_percentage,
        'average_rating': average_rating,
        'total_courses': total_courses
    }
    
    return render(request, 'admin/contents/teachers.html', context)

# views.py da students konteksti
@login_required
def students_view(request):
    students_data = [
        {
            'id': 'ST001',
            'name': 'Azizbek Xolmirzayev',
            'initials': 'AX',
            'email': 'azizbek.x@mail.com',
            'phone': '+998 90 123 45 67',
            'course': 'Python Asoslari',
            'progress': 85,
            'status': 'Aktiv',
            'status_color': 'success',
            'lessons_completed': 18,
            'assignments': 12,
            'rating': 4.8,
            'join_date': '15.01.2024',
            'color': 'primary'
        },
        {
            'id': 'ST002',
            'name': 'Sevara Alimova',
            'initials': 'SA',
            'email': 'sevara.a@mail.com',
            'phone': '+998 91 234 56 78',
            'course': 'Web Dasturlash',
            'progress': 72,
            'status': 'Aktiv',
            'status_color': 'success',
            'lessons_completed': 24,
            'assignments': 15,
            'rating': 4.9,
            'join_date': '22.12.2023',
            'color': 'success'
        },
        {
            'id': 'ST003',
            'name': 'Javohir Tursunov',
            'initials': 'JT',
            'email': 'javohir.t@mail.com',
            'phone': '+998 93 345 67 89',
            'course': 'Data Science',
            'progress': 63,
            'status': 'Aktiv',
            'status_color': 'success',
            'lessons_completed': 15,
            'assignments': 8,
            'rating': 4.7,
            'join_date': '10.02.2024',
            'color': 'warning'
        },
        {
            'id': 'ST004',
            'name': 'Dilnoza Xasanova',
            'initials': 'DX',
            'email': 'dilnoza.x@mail.com',
            'phone': '+998 94 456 78 90',
            'course': 'UI/UX Dizayn',
            'progress': 92,
            'status': 'Yakunlagan',
            'status_color': 'info',
            'lessons_completed': 20,
            'assignments': 18,
            'rating': 4.8,
            'join_date': '05.11.2023',
            'color': 'danger'
        },
        {
            'id': 'ST005',
            'name': 'Shoxrux Abdurahmonov',
            'initials': 'SHA',
            'email': 'shoxrux.a@mail.com',
            'phone': '+998 95 567 89 01',
            'course': 'Mobile Development',
            'progress': 45,
            'status': 'Aktiv',
            'status_color': 'success',
            'lessons_completed': 12,
            'assignments': 6,
            'rating': 4.5,
            'join_date': '18.02.2024',
            'color': 'info'
        },
        {
            'id': 'ST006',
            'name': 'Madina Yusupova',
            'initials': 'MY',
            'email': 'madina.y@mail.com',
            'phone': '+998 97 678 90 12',
            'course': 'Python Asoslari',
            'progress': 78,
            'status': 'To\'xtatgan',
            'status_color': 'warning',
            'lessons_completed': 16,
            'assignments': 10,
            'rating': 4.6,
            'join_date': '30.01.2024',
            'color': 'primary'
        }
    ]
    
    # Calculate statistics
    total_students = len(students_data)
    active_students = len([s for s in students_data if s['status'] == 'Aktiv'])
    graduated_students = len([s for s in students_data if s['status'] == 'Yakunlagan'])
    active_percentage = round((active_students / total_students) * 100)
    graduated_percentage = round((graduated_students / total_students) * 100)
    average_progress = round(sum(s['progress'] for s in students_data) / total_students)
    new_students = 3  # Example new students count
    
    context = {
        'students': students_data,
        'total_students': total_students,
        'active_students': active_students,
        'graduated_students': graduated_students,
        'active_percentage': active_percentage,
        'graduated_percentage': graduated_percentage,
        'average_progress': average_progress,
        'new_students': new_students
    }
    
    return render(request, 'admin/contents/students.html', context)

# views.py da analytics konteksti
@login_required
def analytics_view(request):
    context = {
        'top_courses': [
            {
                'name': 'Python Asoslari',
                'rating': 4.8,
                'students': 145,
                'completion': 85,
                'color': 'primary'
            },
            {
                'name': 'Web Dasturlash',
                'rating': 4.9,
                'students': 203,
                'completion': 72,
                'color': 'success'
            },
            {
                'name': 'Data Science',
                'rating': 4.7,
                'students': 98,
                'completion': 63,
                'color': 'warning'
            },
            {
                'name': 'UI/UX Dizayn',
                'rating': 4.8,
                'students': 112,
                'completion': 92,
                'color': 'danger'
            },
            {
                'name': 'Mobile Development',
                'rating': 4.6,
                'students': 76,
                'completion': 45,
                'color': 'info'
            }
        ],
        'recent_activities': [
            {
                'title': 'Yangi talaba qoʻshildi',
                'description': 'Azizbek Xolmirzayev Python kursiga qoʻshildi',
                'time': '10 daqiqa oldin',
                'color': 'success'
            },
            {
                'title': 'Kurs yakunlandi',
                'description': 'Web Dasturlash kursi 24 talaba tomonidan yakunlandi',
                'time': '1 soat oldin',
                'color': 'primary'
            },
            {
                'title': 'Yangi topshiriq',
                'description': 'Data Science kursi uchun yangi loyiha topshirigʻi',
                'time': '3 soat oldin',
                'color': 'warning'
            },
            {
                'title': 'Reyting yangilandi',
                'description': 'Python kursi reytingi 4.9 ga yetdi',
                'time': '5 soat oldin',
                'color': 'info'
            },
            {
                'title': 'Tizim yangilandi',
                'description': 'Platforma yangi funksiyalar bilan yangilandi',
                'time': 'Kecha',
                'color': 'secondary'
            }
        ]
    }
    return render(request, 'admin/contents/analytics.html', context)

# views.py da assignments konteksti
def assignments_view(request):
    context = {
        'assignments': [
            {
                'title': 'Python Final Project',
                'course': 'Python Asoslari',
                'instructor': 'Ali Valiyev',
                'type': 'Loyiha',
                'priority': 'Yuqori',
                'priority_color': 'danger',
                'status': 'Aktiv',
                'status_color': 'success',
                'due_date': '15.03.2024',
                'is_overdue': False,
                'submissions': 24,
                'total_students': 35,
                'submission_rate': 69,
                'completion_rate': 85,
                'avg_grade': '4.7',
                'more_students': 12,
                'color': 'primary'
            },
            {
                'title': 'React Web Application',
                'course': 'Web Dasturlash',
                'instructor': 'Sevara Xolmirzayeva',
                'type': 'Loyiha',
                'priority': 'Oʻrta',
                'priority_color': 'warning',
                'status': 'Tekshirilmoqda',
                'status_color': 'info',
                'due_date': '10.03.2024',
                'is_overdue': True,
                'submissions': 18,
                'total_students': 28,
                'submission_rate': 64,
                'completion_rate': 72,
                'avg_grade': '4.8',
                'more_students': 8,
                'color': 'success'
            },
            {
                'title': 'Data Analysis Task',
                'course': 'Data Science',
                'instructor': 'Javohir Tursunov',
                'type': 'Laboratoriya',
                'priority': 'Oddiy',
                'priority_color': 'success',
                'status': 'Yakunlangan',
                'status_color': 'secondary',
                'due_date': '05.03.2024',
                'is_overdue': False,
                'submissions': 15,
                'total_students': 20,
                'submission_rate': 75,
                'completion_rate': 92,
                'avg_grade': '4.6',
                'more_students': 5,
                'color': 'warning'
            },
            {
                'title': 'Mobile App Design',
                'course': 'Mobile Development',
                'instructor': 'Azizbek Rahimov',
                'type': 'Dizayn',
                'priority': 'Yuqori',
                'priority_color': 'danger',
                'status': 'Aktiv',
                'status_color': 'success',
                'due_date': '20.03.2024',
                'is_overdue': False,
                'submissions': 8,
                'total_students': 15,
                'submission_rate': 53,
                'completion_rate': 45,
                'avg_grade': '4.5',
                'more_students': 7,
                'color': 'info'
            },
            {
                'title': 'UI/UX Portfolio',
                'course': 'UI/UX Dizayn',
                'instructor': 'Dilnoza Xasanova',
                'type': 'Final Loyiha',
                'priority': 'Juda Muhim',
                'priority_color': 'danger',
                'status': 'Kutilmoqda',
                'status_color': 'warning',
                'due_date': '25.03.2024',
                'is_overdue': False,
                'submissions': 12,
                'total_students': 18,
                'submission_rate': 67,
                'completion_rate': 78,
                'avg_grade': '4.9',
                'more_students': 6,
                'color': 'danger'
            },
            {
                'title': 'Database Design',
                'course': 'Backend Development',
                'instructor': 'Shoxrux Abdurahmonov',
                'type': 'Quiz',
                'priority': 'Oddiy',
                'priority_color': 'success',
                'status': 'Yakunlangan',
                'status_color': 'secondary',
                'due_date': '01.03.2024',
                'is_overdue': False,
                'submissions': 22,
                'total_students': 25,
                'submission_rate': 88,
                'completion_rate': 95,
                'avg_grade': '4.7',
                'more_students': 3,
                'color': 'primary'
            }
        ]
    }
    return render(request, 'admin/contents/assignments.html', context)

# views.py da profile va notifications kontekslari
@login_required
def profile_view(request):
    context = {
        'recent_activities': [
            {
                'title': 'Yangi kurs yaratildi',
                'description': 'Python Advanced kursi muvaffaqiyatli yaratildi',
                'time': '2 soat oldin',
                'icon': 'plus-circle',
                'color': 'success'
            },
            {
                'title': 'Talaba qo\'shildi',
                'description': 'Azizbek Xolmirzayev Web Dasturlash kursiga qo\'shildi',
                'time': '5 soat oldin',
                'icon': 'user-plus',
                'color': 'primary'
            },
            {
                'title': 'Topshiriq yakunlandi',
                'description': 'Data Science kursidagi 15 ta topshiriq tekshirildi',
                'time': '1 kun oldin',
                'icon': 'check-circle',
                'color': 'warning'
            },
            {
                'title': 'Tizim yangilandi',
                'description': 'Platforma yangi funksiyalar bilan yangilandi',
                'time': '2 kun oldin',
                'icon': 'sync',
                'color': 'info'
            }
        ],
        'managed_courses': [
            {
                'name': 'Python Asoslari',
                'description': 'Python dasturlash tilini o\'rganish',
                'students': 145,
                'rating': 4.8,
                'status': 'Aktiv',
                'status_color': 'success'
            },
            {
                'name': 'Web Dasturlash',
                'description': 'Modern web technologies',
                'students': 203,
                'rating': 4.9,
                'status': 'Aktiv',
                'status_color': 'success'
            },
            {
                'name': 'Data Science',
                'description': 'Ma\'lumotlar tahlili va ML',
                'students': 98,
                'rating': 4.7,
                'status': 'Yangi',
                'status_color': 'primary'
            },
            {
                'name': 'Mobile Development',
                'description': 'Mobil ilovalar yaratish',
                'students': 76,
                'rating': 4.6,
                'status': 'Aktiv',
                'status_color': 'success'
            }
        ]
    }
    return render(request, 'admin/contents/profile.html', context)

@login_required
def notifications_view(request):
    context = {
        'notifications': [
            {
                'id': 1,
                'title': 'Yangi talaba ro\'yxatdan o\'tdi',
                'message': 'Sevara Alimova Python Asoslari kursiga qo\'shildi',
                'time': '10 daqiqa oldin',
                'read': False,
                'icon': 'user-plus',
                'color': 'success',
                'actions': [
                    {'text': 'Profilni ko\'rish', 'color': 'primary'},
                    {'text': 'Xabar yuborish', 'color': 'outline-primary'}
                ]
            },
            {
                'id': 2,
                'title': 'Topshiriq muddati yaqinlashmoqda',
                'message': 'Web Dasturlash kursidagi "React Project" topshirig\'i 3 kun qoldi',
                'time': '1 soat oldin',
                'read': False,
                'icon': 'exclamation-triangle',
                'color': 'warning',
                'actions': [
                    {'text': 'Topshiriqni ko\'rish', 'color': 'warning'}
                ]
            },
            {
                'id': 3,
                'title': 'Kurs yakunlandi',
                'message': 'Data Science kursi 25 talaba tomonidan muvaffaqiyatli yakunlandi',
                'time': '3 soat oldin',
                'read': True,
                'icon': 'graduation-cap',
                'color': 'info',
                'actions': [
                    {'text': 'Sertifikatlar', 'color': 'info'}
                ]
            },
            {
                'id': 4,
                'title': 'Tizim yangilandi',
                'message': 'Platforma yangi dashboard va analytics funksiyalari bilan yangilandi',
                'time': '5 soat oldin',
                'read': True,
                'icon': 'sync',
                'color': 'primary',
                'actions': []
            },
            {
                'id': 5,
                'title': 'Yangi xabar',
                'message': 'Sizga "O\'qituvchilar" bo\'limida yangi xabar qoldirildi',
                'time': '1 kun oldin',
                'read': True,
                'icon': 'comments',
                'color': 'purple',
                'actions': [
                    {'text': 'Javob berish', 'color': 'primary'}
                ]
            }
        ]
    }
    return render(request, 'admin/contents/notifications.html', context)

# Settings
@login_required
def settings_view(request):
    return render(request, 'admin/contents/settings.html')

