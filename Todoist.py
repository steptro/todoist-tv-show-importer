from todoist.api import TodoistAPI

apiKey = ''
seriesProjectId = ''

# Input
show = str(input('Name of the tv show?\n'))
while show == '':
    print('The name cannot be empty')
    show = str(input(''))

season = str(input('Which season?\n'))
while season == '':
    print('Season cannot be empty')
    season = str(input(''))

start = str(input('First episode (Default 1))\n'))
end = str(input('Last episode (Default 12)\n'))

# Validate input
if start == '':
    start = 1
else:
    start = int(start)

if end == '':
    end = 12
else:
    end = int(end)

if int(start) > int(end):
    raise Exception('Last episode cannot be before the first episode')

# Prepend 0
if len(season) < 2:
    season = '0' + season

# Load api
api = TodoistAPI(apiKey)

# Get all tasks of the 'TV Series' project
tasks = list(filter(
    lambda x: str(x.data['project_id']) == seriesProjectId and (show == x.data['content'][0:-7] or show == x.data['content']),
    api.items.state['items']
))
tasks.sort(key=lambda x: x.data['item_order'], reverse=True)

# Check if show already exists
if len(tasks) > 0:
    order = tasks[0].data['item_order']
else:
    order = None
    api.items.add(show, seriesProjectId, indent=1)

# Create episode names
for i in range(int(start), int(end) + 1):
    if len(str(i)) < 2:
        episodeIndex = '0' + str(i)
    else:
        episodeIndex = str(i)

    # Create episode string
    episode = show + ' S' + season + 'E' + episodeIndex
    print(episode)

    if order is not None:
        api.items.add(episode, seriesProjectId, indent=2, item_order=order)
    else:
        api.items.add(episode, seriesProjectId, indent=2)

# Add episodes to Todoist
api.commit()

print('Episodes have been successfully added!')
