import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment

# Course data 
courses = {
    'AB History': {
        'title': 'Bachelor of Arts in History',
        'strands': {
            'Core': {'Understanding Culture, Society, and Politics': ['History','Society']},
            'HUMSS': {'Philippine Politics and Governance': ['Politics', 'Governance'],
                      'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']},
        }
    },
    'AB Philosophy': {
        'title': 'Bachelor of Arts in Philosophy',
        'strands': {
            'Core': {'Introduction to Philosophy of the Human Person': ['Philosophy', 'Ethics', 'Society']},
            'GAS': {'Trends, Networks, and Critical Thinking in the 21st Century Culture': ['Culture', 'Critical Thinking'],
                    'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']}
        }
    },
    'BFA Industrial Design': {
        'title': 'Bachelor of Fine Arts Major in Industrial Design',
        'strands': {
            'Core': {'Contemporary Philippine Arts from the Regions': ['Visual Arts', 'Culture']},
            'GAS': {'Practical Research 1 and 2 ': ['Research', 'Design'],
                    'Empowerment Technologies': ['Technology', 'Empowerment'],
                    'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']}
        }
    },
    'BFA Painting': {
        'title': 'Bachelor of Fine Arts Major in Painting',
        'strands': {
            'Core': {'Contemporary Philippine Arts from the Regions': ['Visual Arts', 'Culture']},
            'GAS': {'Practical Research 1 and 2 (focused on art research)': ['Research', 'Art'],
                    'Empowerment Technologies': ['Technology', 'Empowerment'],
                    'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']}
        }
    },
    'BFA Sculpture': {
        'title': 'Bachelor of Fine Arts Major in Sculpture',
        'strands': {
            'Core': {'Contemporary Philippine Arts from the Regions': ['Visual Arts', 'Culture']},
            'GAS': {'Practical Research 1 and 2 (focused on art research)': ['Research', 'Art'],
                    'Empowerment Technologies': ['Technology', 'Empowerment'],
                    'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']}
        }
    },
    'BFA Visual Communication': {
        'title': 'Bachelor of Fine Arts Major in Visual Communication',
        'strands': {
            'Core': {'Contemporary Philippine Arts from the Regions': ['Visual Arts', 'Culture'],
                     'Media and Information Literacy': ['Media', 'Information']},
            'GAS': {'Practical Research 1 and 2 ': ['Research', 'Communication', 'Design'],
                    'Empowerment Technologies': ['Technology', 'Empowerment'],
                    'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']}
        }
    },
    'AB Economics' :{
        'title' : 'Bachelor of Arts and Economics', 
        'strands': {
            'Core': {'Statistics and Probablity': ['Statistics'],
                     'General Mathematics': ['Mathematics']},
            'ABM': {'Applied Economics':['Economics'],
                      'Business Finance': ['Finance'],
                      'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']},
            'GAS': {'Pracitcal Researh 1 and 2':['Research', 'Communication', 'Design']}
        }
    },
    'BS Economics': {
        'title' : 'Bachelor of Science in Economics',
        'strands': {
            'Core': {'Statistics and Probablity': ['Statistics'],
                     'General Mathematics': ['Mathematics']},
            'ABM': {'Applied Economics':['Economics'],
                      'Business Finance': ['Finance'],
                      'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']},
            'GAS': {'Pracitcal Researh 1 and 2':['Research', 'Communication', 'Design']}
        }
      
    },
    'AB Psychology' : {
        'title' : 'Bachelor of Arts in Psychology',
        'strands': {
            'Core': {'Personal Development': ['Human Behavior'],
                    'Understanding Culture, Society and Politics': ['Psychology']},
            'HUMMS': {'Community Engagement, Solidarity and Citizenship': ['Ethics']},
            'GAS': {'Practical Research 1 and 2' :['Research']}
        }
    },
    'BS Psychology': {
        'title': 'Bachelor of Science in Psychology',
        'strands': {
            'Core': {'Personal Development': ['Human Behavior'],
                    'Understanding Culture, Society and Politics': ['Psychology']},
            'HUMMS': {'Community Engagement, Solidarity and Citizenship': ['Ethics']},
            'GAS': {'Practical Research 1 and 2' :['Research']}
        }
    },
    'BS Criminology' :{
        'title': 'Bachelor of Science in Criminology',
        'strand': {
            'HUMMS': {'Trends, Networks, and Critical Thinking in the 21st Century Culture': ['Society']},
                    'Community Engagement, Solidarity, and Citizenship' : ['Criminology']
        }
    },
    'AB Political Science': {
        'title': 'Bachelor of Arts in Political Science',
        'strands': {
            'Core': {'Understanding Culture, Society, and Politics': ['Politics', 'Governance', 'Society']},
            'HUMSS': {'Philippine Politics and Governance': ['Politics', 'Governance']},
            'GAS': {'Trends, Networks, and Critical Thinking in the 21st Century Culture': ['Culture', 'Critical Thinking']}
        }
    },
    'AB English': {
        'title': 'Bachelor of Arts in English',
        'strands': {
            'Core': {
                'Oral Communication': ['English', 'Communication'],
                'Reading and Writing': ['English', 'Literature'],
                '21st Century Literature from the Philippines and the World': ['Literature'],
                'English for Academic and Professional Purposes': ['English', 'Communication']
            },
            'HUMSS': {
                'Creative Writing': ['Literature', 'Writing'],
                'Creative Nonfiction': ['Literature', 'Writing']
            }
        }
    },
    'AB Linguistics': {
        'title': 'Bachelor of Arts in Linguistics',
        'strands': {
            'Core': {
                'Oral Communication': ['Linguistics', 'Language', 'Communication'],
                'Reading and Writing': ['Linguistics', 'Language', 'Communication'],
                'Komunikasyon at Pananaliksik sa Wika at Kulturang Filipino': ['Linguistics', 'Language'],
                'English for Academic and Professional Purposes': ['Linguistics', 'Language']
            },
            'HUMSS': {
                'Filipino sa Piling Larang (Akademik)': ['Language', 'Communication']
            }
        }
    },
    'AB Literature': {
        'title': 'Bachelor of Arts in Literature',
        'strands': {
            'Core': {
                '21st Century Literature from the Philippines and the World': ['Literature', 'Writing'],
                'Reading and Writing': ['Literature', 'Writing'],
                'English for Academic and Professional Purposes': ['Literature', 'Writing'],
                'Filipino sa Piling Larang (Akademik)': ['Literature', 'Writing']
            },
            'HUMSS': {
                'Creative Writing': ['Literature', 'Writing'],
                'Creative Nonfiction': ['Literature', 'Writing']
            }
        }
    },
    'AB Anthropology': {
        'title': 'Bachelor of Arts in Anthropology',
        'strands': {
            'Core': {
                'Understanding Culture, Society, and Politics': ['Anthropology', 'Society', 'Culture'],
                'Inquiries, Investigations, and Immersion': ['Research', 'Anthropology']
            },
            'HUMSS': {
                'Disciplines and Ideas in the Social Sciences': ['Anthropology', 'Social Sciences']
            },
            'GAS': {
                'Practical Research 1 and 2': ['Research', 'Anthropology']
            }
        }
    },
    'AB Sociology': {
        'title': 'Bachelor of Arts in Sociology',
        'strands': {
            'Core': {
                'Understanding Culture, Society, and Politics': ['Sociology', 'Society', 'Culture', 'Research'],
                'Inquiries, Investigations, and Immersion': ['Research', 'Sociology']
            },
            'HUMSS': {
                'Disciplines and Ideas in the Social Sciences': ['Sociology', 'Social Sciences']
            },
            'GAS': {
                'Practical Research 1 and 2': ['Research', 'Sociology']
            }
        }
    },
    'AB Filipino': {
        'title': 'Bachelor of Arts in Filipino',
        'strands': {
            'Core': {
                'Komunikasyon at Pananaliksik sa Wika at Kulturang Filipino': ['Filipino', 'Language', 'Literature'],
                'Pagbasa at Pagsusuri ng Iba\'t Ibang Teksto Tungo sa Pananaliksik': ['Filipino', 'Language', 'Literature']
            },
            'HUMSS': {
                'Filipino sa Piling Larang (Akademik)': ['Filipino', 'Language', 'Literature']
            }
        }
    },
    'BSFS': {
        'title': 'Bachelor of Science in Forensic Science',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Forensic Science', 'Investigation', 'Law'],
                'Physical Science': ['Forensic Science', 'Investigation', 'Law']
            },
            'HUMSS': {
                'Trends, Networks, and Critical Thinking in the 21st Century Culture': ['Society', 'Critical Thinking']
            }
        }
    },
    'AB Islamic Studies': {
        'title': 'Bachelor of Arts in Islamic Studies',
        'strands': {
            'Core': {
                'Understanding Culture, Society, and Politics': ['Islamic Studies', 'Religion', 'Culture', 'Society']
            },
            'HUMSS': {
                'Introduction to World Religions and Belief Systems': ['Islamic Studies', 'Religion', 'Culture', 'Society']
            }
        }
    },
    'BS Environmental Science': {
        'title': 'Bachelor of Science in Environmental Science',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Environmental Science', 'Ecology', 'Sustainability'],
                'Physical Science': ['Environmental Science', 'Ecology', 'Sustainability'],
                'Inquiries, Investigations, and Immersion': ['Research', 'Environmental Science']
            },
            'STEM': {
                'Disaster Readiness and Risk Reduction': ['Environmental Science', 'STEM'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']
            }
        }
    },
    'BS Forestry': {
        'title': 'Bachelor of Science in Forestry',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Forestry', 'Environmental Science', 'Ecology'],
                'Physical Science': ['Forestry', 'Environmental Science', 'Ecology']
            },
            'STEM': {
                'Disaster Readiness and Risk Reduction': ['Forestry', 'STEM']
            }
        }
    },
    'BS Fisheries': {
        'title': 'Bachelor of Science in Fisheries',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Fisheries', 'Aquaculture', 'Marine Science'],
                'Physical Science': ['Fisheries', 'Aquaculture', 'Marine Science']
            },
            'STEM': {
                'Disaster Readiness and Risk Reduction': ['Fisheries', 'STEM']
            }
        }
    },
    'BS Geology': {
        'title': 'Bachelor of Science in Geology',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Geology', 'Earth Science', 'Natural Science'],
                'Physical Science': ['Geology', 'Earth Science', 'Natural Science']
            },
            'STEM': {
                'Earth Science': ['Geology', 'STEM'],
                'Disaster Readiness and Risk Reduction': ['Geology', 'STEM']
            }
        }
    },
    'BS Biology': {
        'title': 'Bachelor of Science in Biology',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Biology', 'Life Sciences', 'Research']
            },
            'STEM': {
                'General Biology 1 and 2': ['Biology', 'Life Sciences', 'Research']
            }
        }
    },
    'BS Molecular Biology': {
        'title': 'Bachelor of Science in Molecular Biology',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Molecular Biology', 'Genetics', 'Research']
            },
            'STEM': {
                'General Biology 1 and 2': ['Molecular Biology', 'Genetics', 'Research']
            }
        }
    },
    'BS Physics': {
        'title': 'Bachelor of Science in Physics',
        'strands': {
            'Core': {
                'Physical Science': ['Physics', 'Mechanics', 'Electromagnetism']
            },
            'STEM': {
                'General Physics 1 and 2': ['Physics', 'Mechanics', 'Electromagnetism']
            }
        }
    },
    'BS Applied Physics': {
        'title': 'Bachelor of Science in Applied Physics',
        'strands': {
            'Core': {
                'Physical Science': ['Applied Physics', 'Engineering', 'Technology']
            },
            'STEM': {
                'General Physics 1 and 2': ['Applied Physics', 'Engineering', 'Technology']
            }
        }
    },
    'BS Chemistry': {
        'title': 'Bachelor of Science in Chemistry',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Chemistry', 'Laboratory Science', 'Research'],
                'Physical Science': ['Chemistry', 'Laboratory Science', 'Research']
            },
            'STEM': {
                'General Chemistry 1 and 2': ['Chemistry', 'Laboratory Science', 'Research']
            }
        }
    },
    'BSCS': {
        'title': 'Bachelor of Science in Computer Science',
        'strands': {
            'Core': {
                'Empowerment Technologies': ['Computer Science', 'Programming', 'Software Development']
            },
            'STEM': {
                'Information and Communications Technology': ['Computer Science', 'STEM'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']
            }
        }
    },
    'BSIT': {
        'title': 'Bachelor of Science in Information Technology',
        'strands': {
            'Core': {
                'Empowerment Technologies': ['Information Technology', 'Systems', 'Networks']
            },
            'STEM': {
                'Information and Communications Technology': ['Information Technology', 'STEM'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']
            }
        }
    },
    'BSIS': {
        'title': 'Bachelor of Science in Information Systems',
        'strands': {
            'Core': {
                'Empowerment Technologies': ['Information Systems', 'Business Technology', 'IT Management']
            },
            'ABM': {
                'Business Mathematics': ['Mathematics'],
                'Business Ethics and Social Responsibility': ['Ethics']
            }
        }
    },
    'BS Mathematics': {
        'title': 'Bachelor of Science in Mathematics',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics', 'Statistics'],
                'Statistics and Probability': ['Statistics', 'Research'],
                'Practical Research 1': ['Research'],
                'Practical Research 2': ['Research']
            },
            'STEM': {
                'Pre-Calculus': ['Mathematics'],
                'Basic Calculus': ['Mathematics'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']
            }
        }
    },
    'BS Applied Math': {
        'title': 'Bachelor of Science in Applied Mathematics',
        'strands': {
            'Core': {
                'General Mathematics': ['Applied Mathematics', 'Statistics'],
                'Statistics and Probability': ['Statistics', 'Research']
            },
            'STEM': {
                'Pre-Calculus': ['Applied Mathematics'],
                'Basic Calculus': ['Applied Mathematics']
            }
        }
    },
    'BS Stat': {
        'title': 'Bachelor of Science in Statistics',
        'strands': {
            'Core': {
                'Statistics and Probability': ['Statistics', 'Data Analysis', 'Research'],
                'Practical Research 1': ['Research'],
                'Practical Research 2': ['Research']
            },
            'STEM': {
                'Research Project': ['Statistics', 'Research'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Research', 'Career Advocacy']
            }
        }
    },
    'Bachelor of Science in Agriculture': {
        'title': 'Bachelor of Science in Agriculture',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Agriculture', 'Farming'],
                'Physical Science': ['Agriculture']
            },
            'STEM': {
                'Empowerment Technologies': ['Agriculture'],
                'Applied Economics': ['Economics']
            },
            'ABM': {
                'Applied Economics': ['Economics'],
                'Business Finance': ['Finance']
            }
        }
    },
    'BS Agribusiness': {
        'title': 'Bachelor of Science in Agribusiness',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Agribusiness', 'Management'],
                'Physical Science': ['Agribusiness']
            },
            'ABM': {
                'Applied Economics': ['Economics'],
                'Business Finance': ['Finance']
            },
            'STEM': {
                'Empowerment Technologies': ['Agribusiness']
            }
        }
    },
    'BS Agroforestry': {
        'title': 'Bachelor of Science in Agroforestry',
        'strands': {
            'Core': {
                'Earth and Life Science': ['Agroforestry', 'Environmental Science', 'Sustainability'],
                'Physical Science': ['Agroforestry']
            },
            'STEM': {
                'Disaster Readiness and Risk Reduction': ['Agroforestry']
            }
        }
    },
    'BS Architecture': {
        'title': 'Bachelor of Science in Architecture',
        'strands': {
            'Core': {
                'Contemporary Philippine Arts from the Regions': ['Architecture', 'Design'],
                'Empowerment Technologies': ['Architecture']
            },
            'GAS': {
                'Practical Research 1 and 2 (focused on architectural research)': ['Research']
            }
        }
    },
    'BLA': {
        'title': 'Bachelor in Landscape Architecture',
        'strands': {
            'Core': {
                'Contemporary Philippine Arts from the Regions': ['Landscape Architecture', 'Environmental Design', 'Sustainability'],
                'Empowerment Technologies': ['Landscape Architecture']
            },
            'GAS': {
                'Practical Research 1 and 2 (focused on landscape research)': ['Research']
            }
        }
    },
    'BS Interior Design': {
        'title': 'Bachelor of Science in Interior Design',
        'strands': {
            'Core': {
                'Contemporary Philippine Arts from the Regions': ['Interior Design', 'Visual Arts', 'Applied Arts'],
                'Empowerment Technologies': ['Interior Design']
            },
            'GAS': {
                'Practical Research 1 and 2 ': ['Research']
            }
        }
    },
    'BSA': {
        'title': 'Bachelor of Science in Accountancy',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics'],
                'Entrepreneurship': ['Business']
            },
            'ABM': {
                'Fundamentals of Accountancy, Business, and Management 1 and 2': ['Accountancy', 'Business', 'Management'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']
            }
        }
    },
    'BSACT': {
        'title': 'Bachelor of Science in Accounting Technology',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics']
            },
            'ABM': {
                'Fundamentals of Accountancy, Business, and Management 1 and 2': ['Accountancy', 'Business', 'Management']
            }
        }
    },
    'BSBA': {
        'title': 'Bachelor of Science in Business Administration',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics']
            },
            'ABM': {
                'Organization and Management': ['Management'],
                'Business Finance': ['Finance']
            }
        }
    },
    'BSBA Business Economics': {
        'title': 'Bachelor of Science in Business Administration Major in Business Economics',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics'],
                'Entrepreneurship': ['Business']
            },
            'ABM': {
                'Applied Economics': ['Economics'],
                'Business Finance': ['Finance'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']
            }
        }
    },
    'BSBA Financial Management': {
        'title': 'Bachelor of Science in Business Administration Major in Financial Management',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics'],
                'Entrepreneurship': ['Business']
            },
            'ABM': {
                'Business Finance': ['Finance'],
                'Fundamentals of Accountancy, Business, and Management 1 and 2': ['Accountancy', 'Business', 'Management'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']
            }
        }
    },
    'BSBA Human Resource Development': {
        'title': 'Bachelor of Science in Business Administration Major in Human Resource Development',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics'],
                'Entrepreneurship': ['Business']
            },
            'ABM': {
                'Organization and Management': ['Management'],
                'Business Ethics and Social Responsibility': ['Ethics']
            }
        }
    },
    'BSBA Marketing Management': {
        'title': 'Bachelor of Science in Business Administration Major in Marketing Management',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics'],
                'Entrepreneurship': ['Business']
            },
            'ABM': {
                'Marketing Principles': ['Marketing'],
                'Applied Economics': ['Economics'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']
            }
        }
    },
    'BSBA Operations Management': {
        'title': 'Bachelor of Science in Business Administration Major in Operations Management',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics'],
                'Entrepreneurship': ['Business']
            },
            'ABM': {
                'Organization and Management': ['Management'],
                'Business Finance': ['Finance'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']
            }
        }
    },
    'BS HRM': {
        'title': 'Bachelor of Science in Hotel and Restaurant Management',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics']
            },
            'ABM': {
                'Organization and Management': ['Management'],
                'Applied Economics': ['Economics'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']
            }
        }
    },
    'BS Entrep': {
        'title': 'Bachelor of Science in Entrepreneurship',
        'strands': {
            'Core': {
                'General Mathematics': ['Mathematics'],
                'Business Mathematics': ['Mathematics'],
                'Entrepreneurship': ['Entrepreneurship']
            },
            'ABM': {
                'Principles of Marketing': ['Marketing'],
                'Organization and Management': ['Management'],
                'Work Immersion/Research/Career Advocacy/Culminating Activity': ['Career']
            }
        }
    },

  
}

# Expertise tags 
expertise_tags = [
    'History', 'Culture', 'Society', 'Politics', 'Philosophy', 'Ethics', 'Logic', 
    'Industrial Design', 'Visual Arts', 'Applied Arts', 'Creativity', 'Painting', 
    'Sculpture', 'Media', 'Design', 'Research', 'Career Advocacy', 'Technology', 'Empowerment',
    'Statistics', 'Economics', 'Finance', 'Human Behavior', 'Psychology', 'Criminology',
    'Governance', 'Critical Thinking', 'Literature', 'Communication', 'Language', 'Linguistics',
    'Creative Writing', 'Creative Nonfiction', 'Filipino', 'Forensic Science', 'Investigation',
    'Law', 'Islamic Studies', 'Religion', 'Anthropology', 'Social Sciences', 'Earth and Life Science',
    'Physical Science', 'World Religions and Belief Systems', 'Environmental Science', 'Ecology',
    'Sustainability', 'Forestry', 'Agribusiness', 'Agroforestry', 'Aquaculture', 'Marine Science',
    'Geology', 'Biology', 'Life Sciences', 'Genetics', 'Physics', 'Applied Physics', 'Engineering',
    'Chemistry', 'Laboratory Science', 'Accountancy', 'Business', 'Management', 'Entrepreneurship',
    'Marketing', 'Business Economics', 'Financial Management', 'Human Resource Development',
    'Operations Management', 'Hospitality Management', 'Tourism', 'Medical Technology', 'Midwifery',
    'Nursing', 'Occupational Therapy', 'Pharmacy', 'Physical Therapy', 'Radiologic Technology',
    'Respiratory Therapy', 'Speech-Language Pathology', 'Sports Science', 'Health', 'Maternal Care',
    'Patient Care', 'Rehabilitation', 'Medication', 'Imaging', 'Communication', 'Physical Education',
    'Office Administration', 'Real Estate Management'
]

def process_preferences(prof_preferred_courses, prof_expertise, years_of_teaching):
    # Create a mapping from strands to subjects with tags
    strand_subjects = {}
    for course in prof_preferred_courses:
        course_data = courses[course]
        for strand, subjects in course_data['strands'].items():
            if strand not in strand_subjects:
                strand_subjects[strand] = {}
            strand_subjects[strand].update(subjects)

    # Create a cost matrix based on expertise match and teaching experience
    strands = list(strand_subjects.keys())
    num_strands = len(strands)
    num_expertise = len(prof_expertise)
    cost_matrix = np.zeros((num_expertise, num_strands))

    experience_weight = {
        "1 year": 0.5,
        "2-4 years": 1.0,
        "5-8 years": 1.5,
        "9 or more years": 2.0
    }

    for i, expertise in enumerate(prof_expertise):
        for j, strand in enumerate(strands):
            for subject, tags in strand_subjects[strand].items():
                if expertise in tags:
                    cost_matrix[i, j] += 1 * experience_weight[years_of_teaching]
                else:
                    # Add a small score for partial matches
                    partial_match_score = len(set(tags) & set(prof_expertise)) * 0.1
                    cost_matrix[i, j] += partial_match_score * experience_weight[years_of_teaching]

    # Apply Hungarian Algorithm to find the optimal assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix, maximize=True)

    # Create the assignment result
    assignment_result = {}

    for i, j in zip(row_ind, col_ind):
        expertise = prof_expertise[i]
        strand = strands[j]
        
        if strand not in assignment_result:
            assignment_result[strand] = {}
        
        # Find the best matching subject for this expertise and strand
        best_subject = None
        best_score = 0
        for subject, tags in strand_subjects[strand].items():
            score = len(set(tags) & set(prof_expertise))  # Count matching tags
            if score > best_score:
                best_score = score
                best_subject = subject
        
        if best_subject and best_subject not in assignment_result[strand]:
            assignment_result[strand][best_subject] = strand_subjects[strand][best_subject]

    # Ensure each strand has at least two subjects if possible
    for strand in strands:
        if strand not in assignment_result:
            assignment_result[strand] = {}
        
        while len(assignment_result[strand]) < 2:
            remaining_subjects = set(strand_subjects[strand].keys()) - set(assignment_result[strand].keys())
            if not remaining_subjects:
                break
            
            best_subject = None
            best_score = 0
            for subject in remaining_subjects:
                score = len(set(strand_subjects[strand][subject]) & set(prof_expertise))
                if score > best_score:
                    best_score = score
                    best_subject = subject
            
            if best_subject:
                assignment_result[strand][best_subject] = strand_subjects[strand][best_subject]
            else:
                # If no match found, assign a subject with the most overlapping tags
                best_subject = max(remaining_subjects, key=lambda s: len(set(strand_subjects[strand][s]) & set(expertise_tags)))
                assignment_result[strand][best_subject] = strand_subjects[strand][best_subject]

    # If no assignments were made, assign subjects based on course preferences
    if not any(assignment_result.values()):
        for course in prof_preferred_courses:
            course_data = courses[course]
            for strand, subjects in course_data['strands'].items():
                if strand not in assignment_result:
                    assignment_result[strand] = {}
                for subject, tags in subjects.items():
                    if subject not in assignment_result[strand]:
                        assignment_result[strand][subject] = tags
                        if len(assignment_result[strand]) >= 2:
                            break
                if len(assignment_result[strand]) >= 2:
                    break

    return assignment_result
# The following functions are kept for reference or potential future use,
# but they are not directly used in the web application

def display_expertise_and_courses():
    print("\nExpertise Tags:")
    for tag in expertise_tags:
        print(f"- {tag}")
    print("\nCourses:")
    for course, data in courses.items():
        print(f"- {course}: {data['title']}")

def choose_preferences():
    print("Welcome! Let's choose your expertise and preferred courses.")
    display_expertise_and_courses()
    
    prof_preferred_courses = []
    while True:
        course = input("Enter your preferred course from the above list: ").strip()
        if course in courses:
            prof_preferred_courses.append(course)
        else:
            print("Invalid course. Please enter a valid course code.")
        more_courses = input("Do you want to add another course? (yes/no): ").strip().lower()
        if more_courses != 'yes':
            break
    
    prof_expertise = []
    while True:
        expertise = input("Enter your expertise tag from the above list: ").strip()
        if expertise in expertise_tags:
            prof_expertise.append(expertise)
        else:
            print("Invalid expertise. Please enter a valid expertise tag.")
        more_expertise = input("Do you want to add another expertise tag? (yes/no): ").strip().lower()
        if more_expertise != 'yes':
            break
    
    teaching_experience_levels = ["1 year", "2-4 years", "5-8 years", "9 or more years"]
    print("\nTeaching Experience Levels:")
    for level in teaching_experience_levels:
        print(f"- {level}")
    
    while True:
        years_of_teaching = input("Enter your teaching experience level from the above list: ").strip()
        if years_of_teaching in teaching_experience_levels:
            break
        else:
            print("Invalid experience level. Please enter a valid option.")

    return prof_preferred_courses, prof_expertise, years_of_teaching

def generate_bipartite_graph(assignment_result):
    B = nx.Graph()
    B.add_node('Professor', bipartite=0)

    for strand, subjects in assignment_result.items():
        B.add_node(strand, bipartite=1)
        B.add_edge('Professor', strand)
        for subject in subjects:
            B.add_node(subject, bipartite=2)
            B.add_edge(strand, subject)

    plt.figure(figsize=(12, 8))
    pos = {}
    pos['Professor'] = (0, 0)
    for i, strand in enumerate(assignment_result.keys()):
        pos[strand] = (1, i)
        for j, subject in enumerate(assignment_result[strand]):
            pos[subject] = (2, i + j * 0.1)

    nx.draw(B, pos, with_labels=True, labels={node: node for node in B.nodes()}, node_color='skyblue', node_size=1500)
    nx.draw_networkx_edges(B, pos, edgelist=B.edges(), width=1.0, alpha=0.5)

    plt.title('Bipartite Graph of Professor Preferences, Strands, and Subjects')
    plt.show()

if __name__ == '__main__':
    # This block is for testing the algorithm independently
    prof_preferred_courses, prof_expertise, years_of_teaching = choose_preferences()
    result = process_preferences(prof_preferred_courses, prof_expertise, years_of_teaching)
    
    print("\nAssignment Result:")
    for strand, subjects in result.items():
        print(f"Strand: {strand}")
        for subject, tags in subjects.items():
            print(f"  - {subject} (Tags: {', '.join(tags)})")
    
    generate_bipartite_graph(result)