-- Sample data for unified resume platform (Supabase / PostgreSQL)
-- Run this in the Supabase SQL Editor AFTER supabase_schema.sql.

-- Resume data

INSERT INTO resumes (resume_title, resume_text, candidate_name, candidate_email, candidate_phone, experience_years, current_position, location) VALUES

('Senior Software Architect - Cloud & Microservices Expert', 'ALEX JOHNSON
Email: alex.johnson@email.com | Phone: (555) 111-2222 | LinkedIn: linkedin.com/in/alexjohnson

PROFESSIONAL SUMMARY
Innovative Software Architect with 10+ years designing enterprise-scale applications. Expert in microservices architecture, cloud infrastructure, and distributed systems. Led technical teams of 15+ engineers delivering solutions for Fortune 500 companies.

TECHNICAL SKILLS
Languages: Java, Python, Go, JavaScript, C++, Scala
Frameworks: Spring Boot, Django, React, Angular, Node.js
Architecture: Microservices, Event-Driven, Serverless
Cloud: AWS, Azure, Google Cloud Platform
Databases: PostgreSQL, MongoDB, Redis, Cassandra
DevOps: Docker, Kubernetes, Terraform, Jenkins
Messaging: Kafka, RabbitMQ, AWS SQS/SNS

EXPERIENCE
Principal Software Architect | CloudTech Enterprises | 2020 - Present
• Architected microservices platform serving 10M+ users with 99.99% uptime
• Led migration from monolithic to microservices reducing deployment time by 80%
• Designed event-driven architecture processing 5M+ events daily
• Mentored 8 senior engineers on system design patterns

Senior Software Engineer | TechInnovate Solutions | 2017 - 2020
• Designed RESTful APIs serving 2M+ requests per day
• Built real-time data processing pipeline using Kafka and Spark
• Optimized database queries reducing response time from 2s to 200ms

EDUCATION
MS Computer Science | Stanford University | 2014
BS Computer Engineering | MIT | 2012

CERTIFICATIONS
AWS Certified Solutions Architect - Professional
Google Cloud Professional Cloud Architect', 'Alex Johnson', 'alex.johnson@email.com', '(555) 111-2222', 10, 'Principal Software Architect', 'Seattle, WA'),

('Senior UX/UI Designer - Product Design & Research', 'MARIA SANTOS
Email: maria.santos@email.com | Phone: (555) 222-3333 | Portfolio: mariasantos.design

PROFESSIONAL SUMMARY
Award-winning Product Designer with 8+ years creating user-centered digital experiences. Specialized in UX/UI design, user research, and design systems. Led design initiatives for products used by 5M+ users.

DESIGN SKILLS
Design: UI/UX Design, Interaction Design, Visual Design, Prototyping
Research: User Research, Usability Testing, A/B Testing
Tools: Figma, Sketch, Adobe Creative Suite, InVision, Principle
Development: HTML/CSS, JavaScript, Design Systems
Methodologies: Design Thinking, Agile/Scrum, Lean UX

EXPERIENCE
Senior Product Designer | DesignFirst Tech | 2019 - Present
• Lead designer for flagship product serving 5M+ active users
• Conducted 100+ user research sessions informing product strategy
• Designed company-wide design system used by 20+ designers
• Improved user onboarding completion rate from 45% to 78%
• Led accessibility initiative achieving WCAG 2.1 AA compliance

Product Designer | UserCentric Apps | 2017 - 2019
• Designed mobile and web applications for multiple platforms
• Improved app store rating from 3.2 to 4.7 stars through UX improvements
• Conducted usability testing sessions with 50+ participants

EDUCATION
MFA Interaction Design | Carnegie Mellon University | 2016
BA Graphic Design | Rhode Island School of Design | 2014

AWARDS
Webby Award Winner - Best User Experience, 2023', 'Maria Santos', 'maria.santos@email.com', '(555) 222-3333', 8, 'Senior Product Designer', 'San Francisco, CA'),

('Lead Data Scientist - ML & AI Expert', 'JAMES CHEN
Email: james.chen@email.com | Phone: (555) 333-4444

PROFESSIONAL SUMMARY
Strategic Data Science Leader with 9+ years building ML models and data-driven solutions. Expert in machine learning, deep learning, and statistical analysis. Led data science teams delivering $20M+ in business value.

TECHNICAL SKILLS
Programming: Python, R, SQL, Scala, Java
ML/DL: TensorFlow, PyTorch, Scikit-learn, Keras, XGBoost
Big Data: Spark, Hadoop, Hive, Databricks
Cloud: AWS SageMaker, GCP BigQuery, Azure ML
Databases: PostgreSQL, MongoDB, Redshift, Snowflake
Visualization: Tableau, Power BI, Matplotlib
MLOps: MLflow, Kubeflow, Docker, Kubernetes

EXPERIENCE
Lead Data Scientist | AI Innovations Inc. | 2020 - Present
• Lead team of 8 data scientists building ML recommendation systems
• Developed deep learning model improving accuracy by 35%
• Built NLP pipeline processing 10M+ customer reviews
• Implemented MLOps infrastructure reducing deployment time by 70%
• Generated $15M additional revenue through personalization

Senior Data Scientist | DataDriven Solutions | 2017 - 2020
• Built predictive models reducing customer churn by 25%
• Developed computer vision system with 98% accuracy
• Created fraud detection system saving $5M annually

EDUCATION
PhD Computer Science (ML) | Stanford University | 2015
MS Statistics | UC Berkeley | 2012
BS Mathematics | MIT | 2010', 'James Chen', 'james.chen@email.com', '(555) 333-4444', 9, 'Lead Data Scientist', 'San Francisco, CA'),

('Senior Product Manager - B2B SaaS', 'SOPHIA WILLIAMS
Email: sophia.williams@email.com | Phone: (555) 444-5555

PROFESSIONAL SUMMARY
Results-driven Product Manager with 7+ years launching successful digital products. Expert in product strategy, roadmap planning, and cross-functional team leadership. Launched 10+ products generating $50M+ in revenue.

SKILLS
Product Management: Strategy, Roadmap Planning, Feature Prioritization
Methodologies: Agile/Scrum, Lean Startup, Design Thinking
Analytics: Google Analytics, Mixpanel, Amplitude, SQL, A/B Testing
Tools: JIRA, Confluence, Productboard, Figma, Miro
Research: User Research, Competitive Analysis, Go-to-Market

EXPERIENCE
Senior Product Manager | TechVentures Inc. | 2020 - Present
• Own product strategy for B2B SaaS platform ($30M ARR)
• Launched 5 major features increasing user engagement by 60%
• Led cross-functional team of 12 members
• Increased product revenue by 45% through strategic development
• Conducted 50+ customer interviews informing direction

Product Manager | InnovateTech Solutions | 2018 - 2020
• Managed mobile app product with 2M+ active users
• Launched new product line generating $10M in first year
• Improved app store rating from 3.8 to 4.6 stars

EDUCATION
MBA | Stanford Graduate School of Business | 2017
BS Computer Science | UC Berkeley | 2015', 'Sophia Williams', 'sophia.williams@email.com', '(555) 444-5555', 7, 'Senior Product Manager', 'San Francisco, CA'),

('Staff Backend Engineer - Distributed Systems', 'MICHAEL BROWN
Email: michael.brown@email.com | Phone: (555) 555-6666

PROFESSIONAL SUMMARY
Expert Backend Engineer with 8+ years building scalable, high-performance systems. Specialized in distributed systems, database optimization, and API design. Built infrastructure serving 50M+ requests daily.

TECHNICAL SKILLS
Languages: Python, Go, Java, JavaScript, Ruby, Rust
Frameworks: Django, Flask, FastAPI, Spring Boot, Express.js
Databases: PostgreSQL, MySQL, MongoDB, Redis, Cassandra
Message Queues: RabbitMQ, Apache Kafka, AWS SQS
APIs: REST, GraphQL, gRPC, WebSockets
Cloud: AWS EC2, Lambda, RDS, S3, GCP, Azure
DevOps: Docker, Kubernetes, Terraform, Jenkins
Monitoring: Prometheus, Grafana, ELK Stack

EXPERIENCE
Staff Backend Engineer | ScaleUp Technologies | 2021 - Present
• Architect backend systems serving 50M+ daily requests
• Designed microservices architecture for core platform
• Optimized database queries reducing response time by 85%
• Built real-time notification system delivering 10M+ notifications
• Implemented caching strategy reducing database load by 60%

Senior Backend Engineer | CloudServices Inc. | 2018 - 2021
• Developed RESTful APIs using Python Django and Flask
• Built data processing pipeline handling 5M+ records daily
• Implemented OAuth 2.0 authentication system
• Optimized API performance reducing latency from 500ms to 50ms

EDUCATION
BS Computer Science | University of Texas at Austin | 2016', 'Michael Brown', 'michael.brown@email.com', '(555) 555-6666', 8, 'Staff Backend Engineer', 'San Francisco, CA'),

('Engineering Manager - Team Leadership', 'EMILY RODRIGUEZ
Email: emily.rodriguez@email.com | Phone: (555) 666-7777

PROFESSIONAL SUMMARY
Dynamic Engineering Manager with 6+ years leading high-performing software teams. Expert in team building, technical mentorship, and agile delivery. Managed teams of 15+ engineers delivering critical business initiatives.

LEADERSHIP SKILLS
Team Building, Performance Management, Career Development
Software Architecture, Code Review, Technical Strategy
Agile/Scrum, Kanban, Continuous Delivery
Hiring, Onboarding, 1-on-1s, Goal Setting
Cross-functional Collaboration, Stakeholder Management

EXPERIENCE
Engineering Manager | TechCorp Global | 2021 - Present
• Manage team of 15 software engineers across multiple disciplines
• Grew team from 8 to 15 members through strategic hiring
• Improved team velocity by 40% through process improvements
• Reduced employee turnover from 25% to 5%
• Established career development framework
• Led successful delivery of 3 major product launches

Senior Software Engineer → Tech Lead | InnovateSoft | 2018 - 2021
• Promoted from Senior Engineer to Tech Lead managing team of 6
• Led technical design and architecture decisions
• Mentored junior engineers through code reviews
• Reduced production incidents by 60%

EDUCATION
MS Computer Science | Stanford University | 2016
BS Computer Engineering | MIT | 2014

CERTIFICATIONS
Certified Scrum Master (CSM)
AWS Certified Solutions Architect', 'Emily Rodriguez', 'emily.rodriguez@email.com', '(555) 666-7777', 6, 'Engineering Manager', 'San Francisco, CA'),

('Senior Frontend Engineer - React & TypeScript', 'DAVID KUMAR
Email: david.kumar@email.com | Phone: (555) 777-8888

PROFESSIONAL SUMMARY
Creative Frontend Engineer with 7+ years building performant web applications. Expert in React, TypeScript, and modern JavaScript. Built user interfaces used by 10M+ users. Strong background in web performance and accessibility.

TECHNICAL SKILLS
Languages: JavaScript ES6+, TypeScript, HTML5, CSS3, Python
Frameworks: React, Next.js, Vue.js, Angular, Redux
Styling: CSS3, Sass/SCSS, Styled Components, Tailwind CSS
Build Tools: Webpack, Vite, Rollup, Babel, ESLint
Testing: Jest, React Testing Library, Cypress, Playwright
Performance: Web Vitals, Lighthouse, Code Splitting
Tools: Git, npm/yarn, Figma, Storybook
Backend: Node.js, Express, REST APIs, GraphQL
Cloud: AWS S3, CloudFront, Vercel, Netlify

EXPERIENCE
Senior Frontend Engineer | WebTech Solutions | 2020 - Present
• Lead frontend development for SaaS platform serving 5M+ users
• Improved application performance by 70% through optimization
• Reduced bundle size by 50% through code splitting
• Implemented design system used across 20+ applications
• Achieved 100% Lighthouse scores for performance and accessibility

Frontend Engineer | DigitalCraft Inc. | 2018 - 2020
• Built responsive web applications using React and TypeScript
• Developed reusable component library with Storybook
• Implemented state management using Redux and Context API
• Achieved 85% test coverage with unit and integration tests

EDUCATION
BS Computer Science | UC Berkeley | 2017
Minor in Design | GPA: 3.7/4.0

CERTIFICATIONS
AWS Certified Developer - Associate
Meta Frontend Developer Professional Certificate', 'David Kumar', 'david.kumar@email.com', '(555) 777-8888', 7, 'Senior Frontend Engineer', 'San Francisco, CA');

-- Job descriptions data

INSERT INTO job_descriptions (job_title, job_description_text, company_name, department, employment_type, experience_required, salary_range, location, posted_by) VALUES

('Principal Software Architect', 'We are seeking an experienced Principal Software Architect to lead our cloud infrastructure initiatives. The ideal candidate will have 8+ years of experience in designing scalable microservices architectures and leading engineering teams.

RESPONSIBILITIES:
• Design and implement enterprise-scale microservices architecture
• Lead technical decision-making for cloud infrastructure (AWS, Azure, GCP)
• Mentor senior engineers and establish technical standards
• Collaborate with product teams on system design and architecture
• Optimize system performance and ensure 99.9% uptime
• Drive adoption of DevOps practices and CI/CD pipelines

REQUIRED SKILLS:
• 8+ years of software architecture experience
• Expert knowledge of Java, Python, or Go
• Strong experience with microservices and distributed systems
• Proficiency in cloud platforms (AWS preferred)
• Experience with Docker, Kubernetes, and container orchestration
• Knowledge of message queues (Kafka, RabbitMQ)
• Database design experience (PostgreSQL, MongoDB, Redis)
• Leadership experience managing technical teams

PREFERRED QUALIFICATIONS:
• Masters degree in Computer Science or related field
• AWS Solutions Architect certification
• Experience with event-driven architecture
• Knowledge of monitoring tools (Prometheus, Grafana)
• Previous experience in high-growth tech companies', 'TechCorp Solutions', 'Engineering', 'full-time', '8+ years', '$180,000 - $250,000', 'Seattle, WA', 'hr@techcorp.com'),

('Senior UX Designer', 'Join our design team as a Senior UX Designer to create exceptional user experiences for our digital products. We are looking for a creative professional with 5+ years of experience in user-centered design and research.

RESPONSIBILITIES:
• Lead UX design for web and mobile applications
• Conduct user research and usability testing
• Create wireframes, prototypes, and high-fidelity designs
• Collaborate with product managers and engineers
• Develop and maintain design systems
• Advocate for accessibility and inclusive design practices
• Mentor junior designers and provide design guidance

REQUIRED SKILLS:
• 5+ years of UX/UI design experience
• Proficiency in Figma, Sketch, and Adobe Creative Suite
• Strong portfolio demonstrating user-centered design process
• Experience with user research methodologies
• Knowledge of HTML/CSS and responsive design principles
• Understanding of accessibility standards (WCAG 2.1)
• Excellent communication and presentation skills
• Experience working in Agile development environments

PREFERRED QUALIFICATIONS:
• Degree in Design, HCI, or related field
• Experience with design systems and component libraries
• Knowledge of front-end development (HTML, CSS, JavaScript)
• Experience with A/B testing and data-driven design
• Previous experience in SaaS or consumer products', 'DesignHub Inc', 'Product Design', 'full-time', '5+ years', '$120,000 - $160,000', 'San Francisco, CA', 'design@designhub.com'),

('Data Science Manager', 'We are seeking a Data Science Manager to lead our analytics team and drive data-driven decision making across the organization. The ideal candidate will have 6+ years of data science experience with 2+ years in a leadership role.

RESPONSIBILITIES:
• Lead team of 5-8 data scientists and analysts
• Develop machine learning models for business applications
• Collaborate with product and engineering teams on data initiatives
• Establish data science best practices and methodologies
• Present insights and recommendations to executive leadership
• Manage hiring and professional development of team members
• Drive adoption of MLOps practices and model deployment

REQUIRED SKILLS:
• 6+ years of data science experience
• 2+ years of team management experience
• Expert knowledge of Python, R, and SQL
• Experience with machine learning frameworks (TensorFlow, PyTorch)
• Strong statistical analysis and modeling skills
• Experience with big data technologies (Spark, Hadoop)
• Knowledge of cloud platforms (AWS, GCP, Azure)
• Excellent communication and leadership skills

PREFERRED QUALIFICATIONS:
• PhD in Computer Science, Statistics, or related field
• Experience with deep learning and NLP
• Knowledge of MLOps tools (MLflow, Kubeflow)
• Experience in recommendation systems or personalization
• Previous experience in e-commerce or consumer tech', 'DataDriven Analytics', 'Data Science', 'full-time', '6+ years', '$160,000 - $220,000', 'New York, NY', 'careers@datadriven.com'),

('Senior Product Manager', 'We are looking for a Senior Product Manager to own the product strategy and roadmap for our B2B SaaS platform. The ideal candidate will have 5+ years of product management experience with a track record of launching successful products.

RESPONSIBILITIES:
• Define product vision and strategy for core platform
• Manage product roadmap and feature prioritization
• Collaborate with engineering, design, and sales teams
• Conduct market research and competitive analysis
• Gather and analyze customer feedback and usage data
• Lead go-to-market initiatives for new features
• Define and track key product metrics and KPIs

REQUIRED SKILLS:
• 5+ years of product management experience
• Experience with B2B SaaS products
• Strong analytical skills and data-driven decision making
• Proficiency with product management tools (JIRA, Confluence)
• Experience with Agile development methodologies
• Excellent communication and stakeholder management skills
• Understanding of technical concepts and API design
• Customer-focused mindset with user research experience

PREFERRED QUALIFICATIONS:
• MBA or technical degree
• Experience with enterprise software
• Knowledge of SQL and data analysis
• Certified Scrum Product Owner (CSPO)
• Previous experience in high-growth startups
• Experience with A/B testing and experimentation', 'ProductFirst Solutions', 'Product Management', 'full-time', '5+ years', '$140,000 - $180,000', 'Austin, TX', 'pm@productfirst.com'),

('Staff Backend Engineer', 'Join our engineering team as a Staff Backend Engineer to build scalable, high-performance systems. We are seeking an experienced engineer with 7+ years of backend development experience and expertise in distributed systems.

RESPONSIBILITIES:
• Design and implement scalable backend services and APIs
• Optimize database performance and query efficiency
• Build real-time data processing pipelines
• Implement caching strategies and performance optimizations
• Collaborate with frontend teams on API design
• Mentor junior and mid-level engineers
• Participate in on-call rotation and incident response

REQUIRED SKILLS:
• 7+ years of backend development experience
• Expert knowledge of Python, Go, or Java
• Strong experience with RESTful API design
• Database expertise (PostgreSQL, MySQL, MongoDB)
• Experience with message queues (RabbitMQ, Kafka)
• Knowledge of caching systems (Redis, Memcached)
• Understanding of microservices architecture
• Experience with cloud platforms and containerization

PREFERRED QUALIFICATIONS:
• Computer Science degree or equivalent experience
• Experience with GraphQL and real-time systems
• Knowledge of DevOps practices and CI/CD
• Experience with monitoring and observability tools
• Previous experience at high-scale companies
• Open source contributions', 'ScaleUp Technologies', 'Engineering', 'full-time', '7+ years', '$170,000 - $230,000', 'San Francisco, CA', 'engineering@scaleup.com'),

('Engineering Manager', 'We are seeking an Engineering Manager to lead our growing development team. The ideal candidate will have 4+ years of software development experience with 2+ years in a leadership role, combining technical expertise with strong people management skills.

RESPONSIBILITIES:
• Manage team of 8-12 software engineers
• Drive technical strategy and architecture decisions
• Conduct 1-on-1s and performance reviews
• Lead hiring and onboarding of new team members
• Collaborate with product and design teams on roadmap planning
• Establish engineering best practices and processes
• Foster team culture and professional development

REQUIRED SKILLS:
• 4+ years of software development experience
• 2+ years of engineering management experience
• Strong technical background in web development
• Experience with Agile development methodologies
• Excellent communication and leadership skills
• Experience with hiring and team building
• Understanding of software architecture and system design
• Ability to balance technical and business priorities

PREFERRED QUALIFICATIONS:
• Computer Science degree or equivalent
• Experience managing remote or distributed teams
• Knowledge of modern development practices (CI/CD, DevOps)
• Previous experience in fast-growing companies
• Certified Scrum Master or similar certification
• Experience with budget and resource planning', 'TechGrowth Corp', 'Engineering', 'full-time', '4+ years', '$150,000 - $200,000', 'Remote', 'mgmt@techgrowth.com'),

('Senior Frontend Developer', 'We are looking for a Senior Frontend Developer to join our web development team. The ideal candidate will have 5+ years of experience building modern web applications with React and TypeScript, with a focus on performance and user experience.

RESPONSIBILITIES:
• Develop responsive web applications using React and TypeScript
• Implement pixel-perfect designs from Figma mockups
• Optimize application performance and bundle sizes
• Write comprehensive unit and integration tests
• Collaborate with designers on component library development
• Ensure cross-browser compatibility and accessibility
• Mentor junior developers and conduct code reviews

REQUIRED SKILLS:
• 5+ years of frontend development experience
• Expert knowledge of React and TypeScript
• Strong proficiency in HTML5, CSS3, and JavaScript ES6+
• Experience with state management (Redux, Context API)
• Knowledge of build tools (Webpack, Vite, Rollup)
• Testing experience (Jest, React Testing Library)
• Understanding of web performance optimization
• Familiarity with version control (Git) and CI/CD

PREFERRED QUALIFICATIONS:
• Experience with Next.js or similar frameworks
• Knowledge of CSS preprocessors (Sass, Less)
• Understanding of accessibility standards (WCAG)
• Experience with design systems and component libraries
• Knowledge of backend technologies (Node.js, REST APIs)
• Previous experience in agile development environments', 'WebCraft Solutions', 'Engineering', 'full-time', '5+ years', '$130,000 - $170,000', 'Seattle, WA', 'frontend@webcraft.com');
