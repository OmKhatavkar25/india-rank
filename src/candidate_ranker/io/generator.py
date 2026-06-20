"""Generates realistic sample data for development and testing."""

from __future__ import annotations

import json
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"

random.seed(42)

CANDIDATES_DATA = [
    {
        "name": "Arjun Mehta",
        "summary": "Senior Software Engineer with 9 years building distributed systems at scale at Uber and Stripe. Expert in Python, Go, and system architecture.",
        "skills": ["Python", "Go", "Kubernetes", "Docker", "AWS", "PostgreSQL", "Redis", "Kafka", "Microservices", "System Design", "gRPC"],
        "total_experience_years": 9,
        "seniority_level": "senior",
        "education": ["B.Tech Computer Science, IIT Bombay"],
        "experience": [
            {"title": "Senior Software Engineer", "company": "Stripe", "duration_years": 4, "description": "Built real-time payment processing pipeline handling $1B+ monthly volume. Designed fault-tolerant distributed system reducing p99 latency by 40%."},
            {"title": "Software Engineer II", "company": "Uber", "duration_years": 3, "description": "Developed ride-matching algorithms serving 1M+ daily requests. Led migration from monolith to microservices architecture."},
            {"title": "Software Engineer", "company": "Flipkart", "duration_years": 2, "description": "Built scalable inventory management system. Optimized database queries reducing load times by 60%."},
        ],
        "behavioral_signals": {"open_source_contributions": 12, "platform_activity_level": "high", "leadership_experience": True, "publications": 2, "speaking_engagements": 4, "collaboration_score": 0.85},
    },
    {
        "name": "Priya Sharma",
        "summary": "Full-stack engineer turned ML specialist. 6 years experience building AI products at Microsoft and a YC startup.",
        "skills": ["Python", "TypeScript", "React", "TensorFlow", "PyTorch", "Azure", "Docker", "NLP", "LLM", "FastAPI", "PostgreSQL"],
        "total_experience_years": 6,
        "seniority_level": "senior",
        "education": ["M.S. Computer Science, Stanford", "B.Tech CSE, IIT Delhi"],
        "experience": [
            {"title": "Machine Learning Engineer", "company": "Microsoft", "duration_years": 3, "description": "Developed NLP models for Azure Cognitive Services. Fine-tuned transformer models achieving state-of-the-art on internal benchmarks."},
            {"title": "Full Stack Engineer", "company": "YC Startup (RapidAI)", "duration_years": 2, "description": "Built ML-powered document processing platform from scratch. Led team of 4 engineers."},
            {"title": "Software Engineer Intern", "company": "Google", "duration_years": 1, "description": "Worked on internal developer tools team. Built CLI tool for automated deployment pipelines."},
        ],
        "behavioral_signals": {"open_source_contributions": 8, "platform_activity_level": "high", "leadership_experience": True, "publications": 3, "speaking_engagements": 2, "collaboration_score": 0.78},
    },
    {
        "name": "Rahul Verma",
        "summary": "DevOps engineer with 8 years in cloud infrastructure, CI/CD, and platform engineering. AWS certified.",
        "skills": ["AWS", "Terraform", "Kubernetes", "Docker", "Jenkins", "Ansible", "Linux", "Bash", "Python", "Prometheus", "Grafana"],
        "total_experience_years": 8,
        "seniority_level": "senior",
        "education": ["B.E. Information Technology, NIT Trichy"],
        "experience": [
            {"title": "Senior DevOps Engineer", "company": "Amazon", "duration_years": 4, "description": "Managed AWS infrastructure for 200+ microservices. Reduced deployment time by 80% through automated CI/CD pipelines."},
            {"title": "Platform Engineer", "company": "Zomato", "duration_years": 2.5, "description": "Built internal developer platform on Kubernetes. Migrated 50+ services to containerized architecture."},
            {"title": "Systems Engineer", "company": "Infosys", "duration_years": 1.5, "description": "Managed Linux server infrastructure for enterprise clients. Automated monitoring and alerting systems."},
        ],
        "behavioral_signals": {"open_source_contributions": 5, "platform_activity_level": "medium", "leadership_experience": False, "publications": 0, "speaking_engagements": 1, "collaboration_score": 0.65},
    },
    {
        "name": "Ananya Patel",
        "summary": "Data Scientist with PhD in ML. 4 years building recommendation systems and predictive models at Spotify and McKinsey.",
        "skills": ["Python", "R", "TensorFlow", "PyTorch", "Spark", "SQL", "Pandas", "NumPy", "Scikit-learn", "Airflow", "A/B Testing"],
        "total_experience_years": 4,
        "seniority_level": "senior",
        "education": ["PhD Machine Learning, CMU", "M.Sc. Statistics, ISI Kolkata"],
        "experience": [
            {"title": "Data Scientist", "company": "Spotify", "duration_years": 2.5, "description": "Built personalization algorithms for Discover Weekly playlists. Improved user engagement by 12% through ML-driven recommendation models."},
            {"title": "Data Science Consultant", "company": "McKinsey & Company", "duration_years": 1.5, "description": "Led data science engagements for Fortune 500 clients. Built predictive models for supply chain optimization."},
        ],
        "behavioral_signals": {"open_source_contributions": 3, "platform_activity_level": "medium", "leadership_experience": False, "publications": 5, "speaking_engagements": 3, "collaboration_score": 0.72},
    },
    {
        "name": "Vikram Singh",
        "summary": "Product Manager with 7 years experience leading B2B SaaS products. Background in computer science and MBA.",
        "skills": ["Product Management", "Agile", "Scrum", "SQL", "Analytics", "A/B Testing", "Python", "JIRA", "Figma", "User Research"],
        "total_experience_years": 7,
        "seniority_level": "manager",
        "education": ["MBA, ISB Hyderabad", "B.Tech Computer Science, DTU"],
        "experience": [
            {"title": "Senior Product Manager", "company": "Atlassian", "duration_years": 3, "description": "Led product strategy for Jira Cloud. Drove 30% revenue growth through new feature launches and user segmentation."},
            {"title": "Product Manager", "company": "Freshworks", "duration_years": 2.5, "description": "Built customer support product from 0 to 500+ customers. Defined roadmap and managed cross-functional team."},
            {"title": "Associate Product Manager", "company": "Microsoft", "duration_years": 1.5, "description": "Worked on Azure DevOps product team. Conducted user research and shipped 15+ features."},
        ],
        "behavioral_signals": {"open_source_contributions": 0, "platform_activity_level": "medium", "leadership_experience": True, "publications": 1, "speaking_engagements": 5, "collaboration_score": 0.90},
    },
    {
        "name": "Neha Gupta",
        "summary": "Frontend engineer specializing in React and TypeScript. 5 years building consumer web applications at high growth startups.",
        "skills": ["React", "TypeScript", "JavaScript", "Next.js", "CSS", "GraphQL", "Jest", "Cypress", "Figma", "Node.js"],
        "total_experience_years": 5,
        "seniority_level": "mid",
        "education": ["B.Tech Computer Science, BITS Pilani"],
        "experience": [
            {"title": "Senior Frontend Engineer", "company": "Razorpay", "duration_years": 2, "description": "Built payment checkout experience used by 10M+ users. Improved conversion rate by 20% through UI/UX optimization."},
            {"title": "Frontend Engineer", "company": "CRED", "duration_years": 2, "description": "Developed credit card management platform. Built real-time notification system using WebSockets."},
            {"title": "Software Engineer", "company": "HackerRank", "duration_years": 1, "description": "Built interactive coding assessment platform. Improved test efficiency through parallel execution."},
        ],
        "behavioral_signals": {"open_source_contributions": 6, "platform_activity_level": "high", "leadership_experience": False, "publications": 0, "speaking_engagements": 2, "collaboration_score": 0.80},
    },
    {
        "name": "Rohit Joshi",
        "summary": "Backend engineer with 10+ years experience in Java, Spring Boot, and distributed systems at fintech companies.",
        "skills": ["Java", "Spring Boot", "Hibernate", "Kafka", "PostgreSQL", "MongoDB", "Docker", "Kubernetes", "Redis", "Microservices"],
        "total_experience_years": 11,
        "seniority_level": "lead",
        "education": ["M.Tech Computer Science, IIT Kanpur", "B.Tech CSE, NIT Surathkal"],
        "experience": [
            {"title": "Lead Backend Engineer", "company": "Groww", "duration_years": 3, "description": "Architected trading platform backend handling 500K requests/second. Led team of 8 engineers."},
            {"title": "Senior Software Engineer", "company": "PhonePe", "duration_years": 4, "description": "Built UPI payment processing system. Implemented fraud detection algorithms reducing chargebacks by 35%."},
            {"title": "Software Engineer", "company": "Oracle", "duration_years": 4, "description": "Developed enterprise database management tools. Optimized query execution engine."},
        ],
        "behavioral_signals": {"open_source_contributions": 2, "platform_activity_level": "low", "leadership_experience": True, "publications": 0, "speaking_engagements": 0, "collaboration_score": 0.70},
    },
    {
        "name": "Sneha Reddy",
        "summary": "ML Engineer focused on computer vision and edge AI. 3 years building production ML systems at Tesla and NVIDIA.",
        "skills": ["Python", "C++", "TensorFlow", "PyTorch", "Computer Vision", "ONNX", "CUDA", "Docker", "MLOps", "AWS"],
        "total_experience_years": 3,
        "seniority_level": "mid",
        "education": ["M.S. Robotics, University of Michigan", "B.Tech ECE, IIIT Hyderabad"],
        "experience": [
            {"title": "ML Engineer", "company": "Tesla", "duration_years": 2, "description": "Developed computer vision models for Autopilot perception stack. Optimized inference pipeline achieving 2x speedup on embedded hardware."},
            {"title": "AI Engineer", "company": "NVIDIA", "duration_years": 1, "description": "Built edge AI deployment toolkit for Jetson platform. Reduced model deployment time by 60%."},
        ],
        "behavioral_signals": {"open_source_contributions": 4, "platform_activity_level": "medium", "leadership_experience": False, "publications": 2, "speaking_engagements": 1, "collaboration_score": 0.68},
    },
    {
        "name": "Karan Malhotra",
        "summary": "Engineering Manager with 12 years experience leading high-performing teams at Google and Meta.",
        "skills": ["Python", "Java", "Distributed Systems", "Leadership", "Agile", "System Design", "Kubernetes", "AWS", "Project Management"],
        "total_experience_years": 12,
        "seniority_level": "manager",
        "education": ["B.Tech Computer Science, IIT Delhi", "MBA, Harvard Business School"],
        "experience": [
            {"title": "Engineering Manager", "company": "Google", "duration_years": 5, "description": "Led 15-person engineering team building Google Cloud infrastructure. Drove key initiatives reducing infrastructure costs by 25%."},
            {"title": "Senior Software Engineer", "company": "Meta", "duration_years": 4, "description": "Built real-time content moderation platform serving 2B+ users. Mentored 10+ junior engineers."},
            {"title": "Software Engineer", "company": "Amazon", "duration_years": 3, "description": "Developed recommendation engine for Amazon Prime Video. Improved user retention by 15%."},
        ],
        "behavioral_signals": {"open_source_contributions": 1, "platform_activity_level": "medium", "leadership_experience": True, "publications": 0, "speaking_engagements": 6, "collaboration_score": 0.92},
    },
    {
        "name": "Deepika Nair",
        "summary": "Data engineer building large-scale data pipelines. 6 years experience with Spark, Airflow, and cloud data warehouses.",
        "skills": ["Python", "Spark", "Airflow", "SQL", "AWS", "Snowflake", "dbt", "Kafka", "Docker", "Terraform"],
        "total_experience_years": 6,
        "seniority_level": "senior",
        "education": ["B.Tech Computer Science, PEC Chandigarh"],
        "experience": [
            {"title": "Senior Data Engineer", "company": "Swiggy", "duration_years": 3, "description": "Built real-time data pipeline processing 500K events/second. Reduced data latency from 1 hour to 5 minutes."},
            {"title": "Data Engineer", "company": "Myntra", "duration_years": 2, "description": "Designed data warehouse architecture for analytics team. Built ETL pipelines serving 50+ dashboards."},
            {"title": "Software Engineer", "company": "Cisco", "duration_years": 1, "description": "Developed network monitoring tools. Built data aggregation pipeline for network metrics."},
        ],
        "behavioral_signals": {"open_source_contributions": 3, "platform_activity_level": "medium", "leadership_experience": False, "publications": 0, "speaking_engagements": 1, "collaboration_score": 0.75},
    },
    {
        "name": "Amit Kumar",
        "summary": "Recent CS graduate passionate about full-stack development. Built several side projects and active open source contributor.",
        "skills": ["JavaScript", "React", "Node.js", "Python", "MongoDB", "Express", "CSS", "HTML", "Git", "REST APIs"],
        "total_experience_years": 1,
        "seniority_level": "junior",
        "education": ["B.Tech Computer Science, SRM University"],
        "experience": [
            {"title": "Software Engineer Intern", "company": "Tech Mahindra", "duration_years": 0.5, "description": "Built internal dashboard for project management using React and Node.js."},
            {"title": "Freelance Developer", "company": "Self-employed", "duration_years": 0.5, "description": "Developed websites for 3 small businesses. Built e-commerce platform using MERN stack."},
        ],
        "behavioral_signals": {"open_source_contributions": 15, "platform_activity_level": "high", "leadership_experience": False, "publications": 0, "speaking_engagements": 0, "collaboration_score": 0.60},
    },
    {
        "name": "Pooja Iyer",
        "summary": "Backend engineer specializing in API design and distributed systems. 4 years building fintech platforms at Coinbase and Razorpay.",
        "skills": ["Go", "Python", "PostgreSQL", "Redis", "Docker", "Kubernetes", "gRPC", "Kafka", "AWS", "Microservices"],
        "total_experience_years": 4,
        "seniority_level": "mid",
        "education": ["B.Tech Computer Science, VIT Vellore"],
        "experience": [
            {"title": "Backend Engineer", "company": "Coinbase", "duration_years": 2, "description": "Built cryptocurrency trading engine processing 100K orders/second. Implemented WebSocket API for real-time market data."},
            {"title": "Backend Engineer", "company": "Razorpay", "duration_years": 2, "description": "Developed payment gateway APIs handling 10M+ transactions monthly. Reduced API latency by 45%."},
        ],
        "behavioral_signals": {"open_source_contributions": 7, "platform_activity_level": "high", "leadership_experience": False, "publications": 0, "speaking_engagements": 2, "collaboration_score": 0.82},
    },
    {
        "name": "Siddharth Chopra",
        "summary": "Solutions architect with 15 years designing enterprise systems. Deep expertise in cloud migrations and system modernization.",
        "skills": ["AWS", "Azure", "GCP", "Terraform", "Java", ".NET", "Python", "Kubernetes", "Microservices", "Enterprise Architecture"],
        "total_experience_years": 15,
        "seniority_level": "principal",
        "education": ["B.E. Computer Science, Thapar University"],
        "experience": [
            {"title": "Principal Solutions Architect", "company": "AWS", "duration_years": 5, "description": "Led cloud migration strategy for Fortune 100 clients. Designed multi-region architectures handling 10M+ users."},
            {"title": "Enterprise Architect", "company": "IBM", "duration_years": 6, "description": "Designed enterprise systems for banking and telecom clients. Led modernization of legacy monoliths to microservices."},
            {"title": "Senior Software Engineer", "company": "Dell", "duration_years": 4, "description": "Developed enterprise management software. Built distributed monitoring system."},
        ],
        "behavioral_signals": {"open_source_contributions": 0, "platform_activity_level": "low", "leadership_experience": True, "publications": 1, "speaking_engagements": 8, "collaboration_score": 0.88},
    },
    {
        "name": "Meera Desai",
        "summary": "AI researcher with expertise in NLP and LLMs. 5 years experience at research labs and building production AI systems.",
        "skills": ["Python", "PyTorch", "TensorFlow", "NLP", "LLM", "Transformers", "Hugging Face", "CUDA", "Docker", "MLflow"],
        "total_experience_years": 5,
        "seniority_level": "senior",
        "education": ["PhD Computer Science (AI), University of Toronto", "M.Sc. AI, University of Edinburgh"],
        "experience": [
            {"title": "Research Scientist", "company": "Google DeepMind", "duration_years": 3, "description": "Published 5 papers on efficient transformer architectures. Contributed to Gemini model development."},
            {"title": "ML Engineer", "company": "Cohere", "duration_years": 2, "description": "Built production LLM serving infrastructure. Optimized inference achieving 3x throughput improvement."},
        ],
        "behavioral_signals": {"open_source_contributions": 10, "platform_activity_level": "high", "leadership_experience": False, "publications": 8, "speaking_engagements": 6, "collaboration_score": 0.76},
    },
    {
        "name": "Ravi Shankar",
        "summary": "Seasoned QA engineer transitioning to DevOps. 8 years experience in test automation and CI/CD pipeline management.",
        "skills": ["Selenium", "Python", "Jenkins", "Docker", "Kubernetes", "AWS", "Linux", "Bash", "JIRA", "Postman"],
        "total_experience_years": 8,
        "seniority_level": "senior",
        "education": ["B.Tech Electronics, Manipal University"],
        "experience": [
            {"title": "Senior QA Engineer", "company": "Adobe", "duration_years": 4, "description": "Built automated testing framework reducing regression test time by 90%. Led QA team of 5."},
            {"title": "QA Engineer", "company": "Flipkart", "duration_years": 3, "description": "Developed end-to-end test suites for e-commerce platform. Integrated testing into CI/CD pipeline."},
            {"title": "QA Engineer", "company": "Accenture", "duration_years": 1, "description": "Manual and automated testing for banking applications."},
        ],
        "behavioral_signals": {"open_source_contributions": 2, "platform_activity_level": "low", "leadership_experience": True, "publications": 0, "speaking_engagements": 0, "collaboration_score": 0.65},
    },
    {
        "name": "Tara Krishnan",
        "summary": "Cybersecurity engineer with 6 years in application security, penetration testing, and security architecture at fintech companies.",
        "skills": ["Python", "Go", "AWS Security", "Kubernetes Security", "Penetration Testing", "IAM", "Cryptography", "Docker", "Linux"],
        "total_experience_years": 6,
        "seniority_level": "mid",
        "education": ["M.Tech Cybersecurity, IIT Madras", "B.Tech CSE, NIT Calicut"],
        "experience": [
            {"title": "Application Security Engineer", "company": "PayPal", "duration_years": 3, "description": "Conducted security audits for 50+ microservices. Implemented automated vulnerability scanning reducing critical issues by 70%."},
            {"title": "Security Engineer", "company": "Cred", "duration_years": 2, "description": "Built security architecture for fintech platform. Led penetration testing engagements."},
            {"title": "Software Engineer", "company": "Cisco", "duration_years": 1, "description": "Developed network security tools. Built firewall rule analysis platform."},
        ],
        "behavioral_signals": {"open_source_contributions": 5, "platform_activity_level": "medium", "leadership_experience": False, "publications": 1, "speaking_engagements": 3, "collaboration_score": 0.72},
    },
    {
        "name": "Aditya Menon",
        "summary": "Platform engineer building developer tools and internal platforms. 7 years experience at Atlassian and GitHub.",
        "skills": ["Go", "TypeScript", "React", "GraphQL", "Docker", "Kubernetes", "PostgreSQL", "Redis", "CI/CD", "API Design"],
        "total_experience_years": 7,
        "seniority_level": "senior",
        "education": ["B.S. Computer Science, UC Berkeley"],
        "experience": [
            {"title": "Senior Platform Engineer", "company": "GitHub", "duration_years": 3, "description": "Built GitHub Actions platform serving 10M+ repositories. Designed scalable workflow execution engine."},
            {"title": "Software Engineer", "company": "Atlassian", "duration_years": 3, "description": "Developed Bitbucket Pipelines CI/CD product. Built plugin ecosystem for marketplace."},
            {"title": "Software Engineer", "company": "Coursera", "duration_years": 1, "description": "Built content delivery platform. Optimized video streaming infrastructure."},
        ],
        "behavioral_signals": {"open_source_contributions": 20, "platform_activity_level": "high", "leadership_experience": False, "publications": 0, "speaking_engagements": 4, "collaboration_score": 0.80},
    },
    {
        "name": "Kavita Joshi",
        "summary": "Mobile engineer with 5 years in React Native and Flutter. Built apps with 10M+ downloads at Swiggy and Ola.",
        "skills": ["React Native", "Flutter", "TypeScript", "JavaScript", "Dart", "Firebase", "Redux", "Jest", "Appium", "REST APIs"],
        "total_experience_years": 5,
        "seniority_level": "mid",
        "education": ["B.Tech Computer Science, NSIT Delhi"],
        "experience": [
            {"title": "Senior Mobile Engineer", "company": "Swiggy", "duration_years": 2.5, "description": "Built React Native app for delivery partners with 1M+ MAU. Improved app performance reducing crash rate by 60%."},
            {"title": "Mobile Engineer", "company": "Ola", "duration_years": 2.5, "description": "Developed rider app features serving 10M+ users. Implemented real-time ride tracking using WebSockets."},
        ],
        "behavioral_signals": {"open_source_contributions": 4, "platform_activity_level": "medium", "leadership_experience": False, "publications": 0, "speaking_engagements": 1, "collaboration_score": 0.70},
    },
    {
        "name": "Manoj Tiwari",
        "summary": "System administrator with 10+ years managing Linux infrastructure. Recently started learning cloud and automation.",
        "skills": ["Linux", "Bash", "Python", "Ansible", "Docker", "Nagios", "Apache", "Nginx", "MySQL", "Postfix"],
        "total_experience_years": 12,
        "seniority_level": "senior",
        "education": ["Diploma in Computer Science", "RHCE Certified"],
        "experience": [
            {"title": "Senior Systems Administrator", "company": "HCL Technologies", "duration_years": 6, "description": "Managed 500+ Linux servers for enterprise clients. Reduced incident response time by 50%."},
            {"title": "Systems Administrator", "company": "Wipro", "duration_years": 4, "description": "Managed datacenter operations. Automated server provisioning using Ansible."},
            {"title": "IT Support Engineer", "company": "Airtel", "duration_years": 2, "description": "Provided Level 2 support for internal IT systems."},
        ],
        "behavioral_signals": {"open_source_contributions": 0, "platform_activity_level": "low", "leadership_experience": False, "publications": 0, "speaking_engagements": 0, "collaboration_score": 0.55},
    },
    {
        "name": "Isha Agarwal",
        "summary": "Engineering leader turned entrepreneur. 14 years building and scaling engineering teams. Founded a startup that was acquired by Google.",
        "skills": ["Python", "Java", "Leadership", "Product Strategy", "System Design", "Cloud Architecture", "Team Building", "Agile"],
        "total_experience_years": 14,
        "seniority_level": "principal",
        "education": ["B.Tech Computer Science, IIT Roorkee", "MBA, Stanford GSB"],
        "experience": [
            {"title": "Founder & CTO", "company": "DataLens (acquired by Google)", "duration_years": 4, "description": "Built AI-powered data analytics platform. Grew engineering team from 0 to 40. Company acquired for $200M."},
            {"title": "Director of Engineering", "company": "Twitter", "duration_years": 3, "description": "Led 60-person engineering organization for ads platform. Drove 30% revenue growth through ML optimization."},
            {"title": "Senior Software Engineer", "company": "Google", "duration_years": 4, "description": "Built Google Ads infrastructure. Led migration from legacy system to cloud-native architecture."},
            {"title": "Software Engineer", "company": "Microsoft", "duration_years": 3, "description": "Developed Azure DevOps platform. Built continuous integration product."},
        ],
        "behavioral_signals": {"open_source_contributions": 3, "platform_activity_level": "medium", "leadership_experience": True, "publications": 0, "speaking_engagements": 10, "collaboration_score": 0.95},
    },
]

JOB_DESCRIPTIONS_DATA = [
    {
        "title": "Senior Software Engineer — Distributed Systems",
        "description": "We are looking for a Senior Software Engineer to join our platform team. You will design and build scalable distributed systems that power our core infrastructure. The ideal candidate has deep experience with microservices architecture, containerization, and cloud-native technologies. Key Responsibilities: Design and implement high-throughput, low-latency distributed systems. Architect microservices decomposition strategy. Optimize database performance at scale. Mentor junior engineers and drive technical decisions. Collaborate with product teams to define technical roadmap. Requirements: 5+ years of software engineering experience. Strong proficiency in Python, Go, or Java. Deep understanding of distributed systems concepts (consistency, partitioning, fault tolerance). Experience with Kubernetes, Docker, and cloud platforms (AWS/GCP). Strong knowledge of databases (SQL and NoSQL). Experience with message queues (Kafka, RabbitMQ). Bachelor's degree in Computer Science or related field. Nice to Have: Experience at high-scale internet companies. Open source contributions. Experience with observability and monitoring systems. Track record of technical leadership.",
    },
    {
        "title": "Machine Learning Engineer — NLP & LLMs",
        "description": "Join our AI team to build and deploy state-of-the-art NLP models and LLM-powered features. You will work on everything from fine-tuning foundation models to building production inference pipelines. Key Responsibilities: Fine-tune and deploy large language models for production use cases. Build scalable ML pipelines for training and inference. Design evaluation frameworks for model quality. Collaborate with product teams to integrate AI features. Contribute to research and publish papers. Requirements: 3+ years of experience in machine learning. Strong Python skills and ML framework experience (PyTorch, TensorFlow). Deep understanding of transformer architectures and attention mechanisms. Experience with NLP techniques and tools. Familiarity with MLOps practices and tools. Experience deploying models to production. MS/PhD in Computer Science, ML, or related field. Nice to Have: Published research at top ML conferences. Experience with LLM fine-tuning (LoRA, RLHF). Experience with distributed training. Open source ML contributions.",
    },
    {
        "title": "DevOps / Platform Engineer",
        "description": "We are scaling our infrastructure and need a Platform Engineer to build the foundation our engineering team relies on. You will own our CI/CD pipelines, cloud infrastructure, and developer experience. Key Responsibilities: Design and maintain CI/CD pipelines. Manage and optimize Kubernetes clusters. Build internal developer platform and tooling. Implement infrastructure as code. Monitor system reliability and performance. Automate operational workflows. Requirements: 4+ years of infrastructure/platform engineering. Strong knowledge of Kubernetes and Docker. Experience with infrastructure as code (Terraform). Deep AWS or GCP knowledge. Scripting skills (Python, Bash). Experience with monitoring and observability tools. Understanding of networking concepts. Nice to Have: Experience at scale (100+ microservices). Contributions to CNCF projects. SRE experience. Security background.",
    },
    {
        "title": "Senior Data Scientist — Recommendation Systems",
        "description": "We are looking for a Senior Data Scientist to drive our recommendation and personalization systems. You will work on algorithms that impact millions of users daily. Key Responsibilities: Design and build recommendation algorithms. Run A/B experiments to validate model improvements. Analyze user behavior data to identify opportunities. Build ML pipelines for training and serving. Communicate findings to stakeholders. Requirements: 4+ years of data science experience. Strong Python and SQL skills. Experience with ML frameworks (scikit-learn, PyTorch, TensorFlow). Deep understanding of recommendation systems. Experience with A/B testing and experiment design. Strong statistical analysis skills. PhD or MS in a quantitative field. Nice to Have: Published research on recommendation systems. Experience with Spark or distributed computing. Domain experience in e-commerce or content platforms. Experience with deep learning for recommendations.",
    },
]


def sanitize_filename(text: str) -> str:
    return text.lower().replace(" ", "_").replace("/", "_").replace("—", "_").replace("__", "_")


def generate_all() -> None:
    jd_dir = DATA_DIR / "job_descriptions"
    jd_dir.mkdir(parents=True, exist_ok=True)
    for jd in JOB_DESCRIPTIONS_DATA:
        fname = sanitize_filename(jd["title"]) + ".json"
        path = jd_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(jd, f, indent=2)
        print(f"  [JD] {path.name}")

    cand_dir = DATA_DIR / "candidates"
    cand_dir.mkdir(parents=True, exist_ok=True)
    for c in CANDIDATES_DATA:
        fname = sanitize_filename(c["name"]) + ".json"
        path = cand_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(c, f, indent=2)
        print(f"  [Candidate] {path.name}")

    print(f"\nGenerated {len(JOB_DESCRIPTIONS_DATA)} job descriptions and {len(CANDIDATES_DATA)} candidates in {DATA_DIR}")


if __name__ == "__main__":
    generate_all()
