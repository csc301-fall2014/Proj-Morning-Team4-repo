## Product
Our group chose to make a Calendar application. With our product, students will be able to view a wide variety of events, from lectures to even birthdays; this all-encompassing tool will allow users to seamlessly manage their schedules on the web. After creating an account, students will have the ability to subscribe to a school and then to courses they are enrolled in. Students will then be able to see their schedules in a web calendar displaying information such as the times and locations of lectures, tutorials and upcoming events.
Our product showcases many unique additional features which set it apart from rival calendar applications. For instance, our product solves the common administrative issue whereby the professor forgets to update the class calendar in a unique way. Our product allows the instructors of each class to nominate “student admins” from the list of students in that course.These student admins are then given extra privileges including the ability to fix course calendar errors and add additional events. Students themselves also have the ability to navigate to the course page and request to become a student admin.
Another notable feature included in our product is the ability to ‘overlay’ course calendars. A user will typically have many different classes and personal calendars on their account and it will be very likely for their main calendar to get crowded. By allowing the user to filter by calendar type the user is able to better manage their schedule.
One final exemplary feature that is unique to our product is our Calendar’s notifications tool. A user will receive notifications to their homepage when the system needs to convey important information such as: a reminder for an upcoming event, or if they have just gained student admin privileges.     

##  Process
### What worked well?
During the planning stages of Phase I our group laid out software development procedures to ensure that we worked effectively as a team. One of the most crucial elements to our team’s success is our use of the “scrum” software development framework. This began by splitting group members up into either “front-end” or “back-end” developers, also by assigning and setting realistic coding tasks for each group member at the beginning of each scrum iteration. The combined tasks would form the milestone for each week. These tasks and milestones would then be logged and recorded on Github. As the week progressed, our group would hold multiple in-person and online scrum meetings to ensure timelines were being met. Our group would also hold informal Facebook chats throughout the week to seek the group’s advice on problems that were encountered.
We found this process to be quite effective. Splitting the group up into front end and back end teams allowed members to specialize and become experts on their respective sections of the product, enhancing the whole group’s collective productivity. Furthermore, we noticed that frequent meetings kept our group abreast of fellow group member’s progress. Members who completed their tasks early could then offer assistance to those who needed it. Additionally, we noticed that holding informal Facebook chats worked quite well as it allowed us to quickly bounce ideas off each other without having to assemble the whole group.
What worked poorly?
One aspect of our process which we initially struggled with was coordinating in person meetings. Each of our group members have a very demanding course schedule making it very difficult to find mutually agreed upon meeting times. Fortunately, we were able to solve this conundrum with the use of our very own Calendar product. Each group member would input their obligations into a calendar and using the “overlay” feature we were able to determine which times worked well for everybody.

If you had to continue and design your process what would it look like? ie ideal process
Since the process our group used worked very well our “ideal” process would likely closely resemble the process we implemented. In a perfect world we would have liked to hold meetings once a day, everyday. Unfortunately, given the time constraints in our lives this is naturally a lofty goal. In a perfect world we would have also appreciated more time for each phase so we would have more time for planning and discussing different approaches


## Architecture
### Process execution structure  

(Ref: http://littlegreenriver.com/weblog/wp-content/uploads/mtv-diagram-730x1024.png)
### Module structure
Django operates using a MVT design framework; as a consequence, objects do not directly call other objects to perform a task. Instead, django’s framework acts as a “controller” by sending requests to the appropriate view, according to the Django URL configuration. Django’s “views” act as an interface between the model functions (explained in the file structure) and the template. 
Our project is separated into 4 different applications where the views are categorized according to their own functionalities:
- __Main + authentication__ handles responsibilities relating to users such as registration and login and creation of all objects owned by a user instance.
- __Scheduler__ handles event and calendar functionalities
- __Courses__ handles the creation and maintenance of school and course objects
- __Notifications__ handles different signals to create the necessary notifications. 

###File structure
####Databases
- Object Relational Mapping: Models belonging to applications whose attributes represent database fields
    - Authentication : UserProfile, Instructor, Student
    - Scheduler: Event, Calendar
    - School: SchoolProfile, CourseProfile
- Notifications: Notification
- Relations: Represent many to many relationships
    - UserProfile_Courses : The courses each user is enrolled in
    - course_student_admins : The admins of each course
- Django models: Used by Django’s built-in features such as authentication
User, user_permission

###Most significant architecture decisions:

####Choosing django framework
__Reasons:__
One (former) team member who was very experienced in Django suggested our group use the framework. Every group member had experience with Python so we thought that learning the Django framework would be relatively simple.
Our group was also driven towards using Django thanks to its object relational mapper which simplified sql queries or tables. 

Good decision?

Initially in the early stages of our project, our group struggled to learn the intricacies of Django, leading us to initially view it as a poor choice of framework. However, by Phase IV, most of the members were comfortable with the framework. Reflecting on the project with the benefit of hindsight, we now view the framework decision in a decisively positive light . Learning an unfamiliar framework not only pushed us to work harder, it also forced us learn a new skillset which we feel will be very useful moving forward. 

“Each mistake teaches you something new about yourself. There is no failure, remember, except in no longer trying. It is the courage to continue that counts.” ― Chris Bradford


###Dividing up the project into four smaller applications:
__Reasons__: Project components were divided up based upon semantic meaning. This lead to a much more intuitively laid out, less cluttered program. This is crucially important when multiple people are working on the same files.

Furthermore, we found dividing up the code into separate applications made the planning of the project much simpler
It also made locating issues picked up on Github much easier 

Good decision?

Dividing up the project into four applications proved to be an excellent idea, allowing for a very smooth coding process.

## Individual Reports

### Carl Gledhill (gledhil8)
- My most significant contrubution was the design and implementation of the "Student Admin" user and related functions (commits 3a131d7c054d817033e1c506442e606dad2daf04 and 0e3e91edc2c41524aabdaaf5c466a7ad327d7403)
- While working on our Calendar website the most significant technical concept I learned was how to use the Django framework and getting comfortable with the MVT design pattern
- My biggest strength as a team member was my ability to communicate with the group and verbalize our groups body of work by writing excellent Process/product reports.
- One thing I could improve on would be breaking up my commits into smaller pieces so fellow group members can be aware of my progress along the way.
### Michael Li (limich17)
### Tommy Li (tommyzli)
- My most significant contribution was the implementation of the user permissions. 
    - https://github.com/csc301-fall2014/Proj-Morning-Team4-repo/blob/master/phase2/csc301_calendar_app/main/models.py
    - https://github.com/csc301-fall2014/Proj-Morning-Team4-repo/blob/master/phase2/csc301_calendar_app/main/utils.py 
- While working on this project, I learned how Django handles user authentication and permissions in the back end. There were many options to choose from, including permission objects and user groups, as well as completely custom permission checks, which I chose.
- One of my strengths was that I stayed very up to date on the team’s progress, in meetings and in group chats to make sure I was not falling behind in anything.
- Something I could improve on is keeping my team members up to date on my progress by communicating more throughout the sprints and through more frequent commits.
### Sang-Ah Han (sangahhan)
- My most significant contribution was the design and implementation of the calendar overlay feature, which was the main feature in relation to one of our milestones (user stories)
    - First functional commit for this feature: commit 6d5c9df85e379db03e3379a488cd214cfcbe975c
- While working on our web application, I learned about how to use AJAX to make real-time client-side updates based on data from the back-end. This technology was used to display notifications for newly-created events & event updates for Student users and student admin requests for Instructor users
    - Tutorials used: http://www.w3schools.com/ajax/, http://api.jquery.com/jquery.ajax/, http://www.w3schools.com/jsref/met_win_setinterval.asp 
    - Skeleton without actual calls to back-end: commit  c244ec14e77ba1bdf4fe8df9d17229414828514d
- I like to keep my development processes well documented and organized. For our project, I created different tasks and milestones which helped us organize and monitor the progress of our team
- I could keep people more informed of what I am doing as well as getting more information from what other people are doing, so I don’t write unnecessary code
### Amrutha Krishnan (AmruthaKris)
- My most significant contribution was with the front end portion admin requests
    - One of my commits: 274ad358242f37ce790200f1604972935916a038
- While working on this project I learned how to work with the Django framework, also how to incorporate Bootstrap into the front-end design portion of the assignment. Also, learned how to properly integrate all the different programs like SQL, Python, html and more together. All of this will possibly help me in future projects.
- I believe my main strength would be in creating an appealing design while working on the front end portion of the assignment.
- My main weakness was with multi-tasking and keeping up with the team’s progress towards the end of the assignment after my laptop broke and I had to switch operating systems. 
### Binuri Walpitagamage(binuri)
- My most significant contribution was the design and implementation of the backend components of the scheduler application.
    - Link to application source code : https://github.com/csc301-fall2014/Proj-Morning-Team4-repo/tree/master/phase2/csc301_calendar_app/scheduler
- While working on our CourseMate webapp, I learned about how Django implements the observer pattern with signals. I used this technique when creating the backend of the notifications feature of our product.
    - Commit for the notification of student admins: https://github.com/csc301-fall2014/Proj-Morning-Team4-repo/commit/f8890c25c5dbdc566799bd144bd78f9c761dadec 
- I tend to learn new concepts fairly quickly. In the beginning, when all the team members were learning the process, this strength came in useful since it gave me the ability to start the initial skeleton of our code base so that everyone else can learn more from it as well as to gradually contribute to it.
    - Initial skeleton commit: https://github.com/csc301-fall2014/Proj-Morning-Team4-repo/commit/44c09c031faf4e95c267583c412eff599c1574a8
- Upon completion of a task, I usually forget to close the related github issues which results in a false progress status for someone looking at our teams github repo. Therefore I should pay more attention to the administrative details and tasks.
