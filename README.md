# PyKickstarter v3.0

This is a Python Library to take advantage of the Kickstarter API. 

### Non-authenticated Features
1. Simple text searching
2. Searches by category
3. Staff Pick listing

### Authenticated Features
1. Browse Starred Projects
2. Browse Backed Projects
3. View and Post Comments
4. Message Project Creators
5. View updates
6. Receive Notifications

Overall, the library provides access to all of the data returned by the API. I created wrapper functions for segments that I found important. It can easily be expanded. In Docs, I've included some sample JSON reponses for different data types to show what is available. 

### Example Use

```python

from PyKickstarter import PyKickstarter

kick = PyKickstarter()

# If you want to log in

kick.login(EMAIL, PASSWORD)
projects = kick.get_backed_projects()

for project in projects.next():
	print project.id
```

### To Do List

1. Investigate the unauthenticated features. The project generator can't reload the list. 
