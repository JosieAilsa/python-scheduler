# Hiring Challenge
Challenge!

## Objectives.
Your goal is to make a task scheduler using the stub code which is incomplete
and doesn't pass the existing tests yet. Please don't fret
about this challenge too much; enjoy it if possible 🤓
We're not looking for a perfect solution or even a complete solution; we just
need something that you've worked on to discuss, that we also understand! So:

- We don't expect you to spend more than 1.5 hours on it including reading time (unless you want to!)
- If you *do* spend more than 1.5 hours on it - please log how long you spend, and tell us how long you spent when you submit
- Please **do not fork this repository** to your own account - it will be visible to other applicants! Use the "**Use this template**" button at the top (and see "How to get started" below, for further recommendations)
- If you don't feel you have enough time to write any code, just record some thoughts about the challenge in code comments or pseudo-code, for example.
- Please try to make **regular, atomic commits** to a **branch** (even if they are WIP (Work In Progress) commits).
- If we go to interview, we'll talk over what you did, and may go into a pairing exercise on it

### Purpose of Tasks and Scheduler

Tasks are run hourly. They will operate on an hour's worth of data (i.e. an hour
"period"), with the start of that period being given as a parameter (`when`).
Ordinarily, this `when` parameter would be set to the **previous complete hour**.


For example, a task running at 08:01 would be given the time 07:00 as
its `when` parameter, which would cover the period of 07:00 to 08:00.


Tasks should be kept up to date so that the latest period they have completed is
for the last fully complete hour, and this time (e.g. 07:00 in the example) is
stored as `latest_done`.


Additionally, Tasks can '**back fill**' to a certain point in the past
(`start_from`), and their progress back in time toward that is stored as
`earliest_done`.

For example, a task that has completed its latest period
should move to back fill an older period until `earliest_done` is the same as
`start_from`.


Tasks may be stopped at a known point in the future by setting `repeat_until`.


The Scheduler is in charge of scheduling the tasks so that they are all kept up
to date, and back filled when there is time to do so. The Scheduler should:
- [x] Store tasks
- [x] Register new tasks
- [ ] Filter tasks to find what needs doing
- [ ] Schedule filtered tasks to prioritise those that have the nearest (i.e. most recent) to-do period right now
- [ ] Schedule filtered tasks to back fill periods when there are no recent to-do periods
- [ ] Scheduled tasks should keep track of their progress (forward and backward in time)

The checked items above are "done", but you may wish to reimplement them.

### Your goals
In order of importance (first is most important):

- Most important - keep 100% test coverage!
- Either complete or re-write, and add to the existing methods in `challenge.py` according to the above description of the purpose.
- Get all existing tests passing

## How to get started

You'll be using `GitHub` and `git` to get started, then either `Docker` or `virtualenv`.

### Copying the code

**Important**: For your privacy, please follow the recommendation here for getting and working on the code.

- If you don't already have one, get a free account with [GitHub](https://github.com/). In the following instructions we assume your user name is `YOUR_USER_NAME`.
- At the top of the [DemandLogic/hire-challenge](https://github.com/DemandLogic/hire-challenge/) repo - click the "[Use this template](https://github.com/DemandLogic/hire-challenge/generate)" button (<-- or just click this link!)
- After clicking you'll get a form where you can choose a name for your copy of the repo. We recommend using one generated from [here](https://www.thisworddoesnotexist.com/). Below, we'll refer to it as `UNIQUE_REPO_NAME`.
- Don't change any of the other options.
- Press the "Create repository from template" button
- On your computer check out the code (e.g. `git clone git@github.com:YOUR_USER_NAME/UNIQUE_REPO_NAME`, or use the GitHub app, etc.)
- Change this `README.md` file to be empty except for the name of your repo (e.g. `# UNIQUE_REPO_NAME`)
- Commit your change: `git add README.md && git commit -m "Empty readme file."`
- Push your change to GitHub `git push origin`
- Make a new branch: `git checkout -b challenge-branch`
- Edit your `README.md` to include your name.
- Commit this change: `git commit -am "Added my name"`
- Push your branch to GitHub: `git push --set-upstream origin challenge-branch`

Having done this you will have a new repo populated with the contents of `hire-challenge`, an `Initial commit` for all files, except the `README.md` for which you will have another commit with the message `Empty readme file.`. You'll have a new branch called `challenge-branch`, with a single new commit `Added my name`.


### Running the code

We provide a `Dockerfile` so that you can build a working container to run the
tests in, but if you can't get `docker` working then you might want to just use
a `virtualenv`.

- Go into the repo directory
- Using Docker:
  - Run `docker build -t dl/hire-challenge .` to build a container which included the environemnt and the code
  - Then run `docker run -it dl/hire-challenge` to run the tests
  - You could also get a shell on the container and run tests manually like so `docker run -it dl/hire-challenge bash` and then run `pytest`
  - And if you don't want to rebuild the container each time you tweak a test, you can use `docker run -it -v $(pwd):/opt/hire-challenge dl/hire-challenge pytest` to mount the current directory into the container (or `docker run -it -v $(pwd):/opt/hire-challenge dl/hire-challenge bash` for a shell with same mount set up)
- Or:
  - Create a `virtualenv`
  - Use `pip install -r requirements.txt` to populate your environment
  - Run tests using `pytest` in the checkout directory

### Finally

Keep committing code on the `challenge-branch` branch on your computer, and push
to GitHub regularly. Once you're done, make a Pull Request (PR) from the branch
into `main` of your repo. If you don't know how to do this, let us know and we
can help. Send us the address of your PR when you're done (or your repo if you
can't make a PR).

## Don't forget

- Create a newly named repo from the `hire-challenge` template
- Commit regularly on the `challenge-branch` branch
- Push your code to GitHub
- Make a Pull Request from `challenge-branch` to `main`
- Send us a link
- Enjoy!
