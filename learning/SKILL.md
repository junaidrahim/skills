---
name: learning-quests
description: Long-term technical deep dives with structured syllabi, deadlines, and creation goals. Use when Junaid wants to systematically learn a topic (compilers, databases, etc.) over a quarter with books, papers, and project outputs.
---

# Learning Quests

Structured technical deep dives over a quarter or a few months.

## Location

- **Quest notes:** `Notes/<Topic>.md` (tagged `#project`)
- **Examples:** `Compilers.md`, `Database Engineering.md`, `AI Native Engineering.md`

## Quest Structure

```markdown
---
Status: Pending | In Progress | Resolved
Quarter: "[[2025, Q3]]"
---

#project

### Outcome

What is supposed to be the outcome of completing this quest?

- Clear statement of what "done" looks like
- Skills/knowledge to gain

### Consumption Agenda

Build a tentative map of all the information you will be exploring/devouring.

- Books
  - Book 1
  - Book 2
- Courses and Talks
  - Course 1
  - Talk 1
- Papers
  - Paper 1
- Other Links
  - Link 1

### Creation Agenda

Build a checklist of all the things you want to create/express to declare this quest as successful.

- [ ] Blog post about X
- [ ] Build Y from scratch
- [ ] Contribute to Z

### Other Notes

(Misc observations, links, ideas)
```

## Workflow

### Starting a New Quest

1. Pick a topic you're curious about
2. Create `Notes/<Topic>.md` with the template above
3. Define the **Outcome** — what does mastery look like?
4. Build **Consumption Agenda** — syllabus of books, courses, papers
5. Define **Creation Agenda** — blog posts, projects, contributions
6. Set **Quarter** deadline
7. Set **Status: In Progress**

### During the Quest

- Work through consumption agenda
- Check off creation items as you complete them
- Add notes and observations to the file
- Blog posts → also tracked in `writing-technical-blogs` skill

### Completing a Quest

- All creation agenda items checked
- Set **Status: Resolved**
- Carry incomplete items to a new quest if needed

## Heartbeat Integration

Periodically check on active quests (`Status: In Progress`):
- "How's the databases deep dive going?"
- "Any progress on the compilers quest?"
- Surface if a quest has been stale for a while

## Setting Up a Calendar

When starting a quest, help break it into a timeline:

1. **Estimate scope** — How many books/courses? How many outputs?
2. **Set milestones** — Monthly or bi-weekly checkpoints
3. **Add to daily notes** — Specific reading/watching sessions
4. **Track in quarterly note** — Link active quests

Example timeline for a quarter:
- **Week 1-4:** Consume Book 1, watch Course 1
- **Week 5-8:** Build Project 1, write Blog Post 1
- **Week 9-12:** Consume Book 2, finish Project 2, write Blog Post 2

## Active Quests (Update as needed)

Check vault for `#project` notes with `Status: In Progress` or `Status: Pending`.

## When Helping

- Help define scope and realistic timelines
- Suggest resources if asked
- Break large agendas into weekly chunks
- Don't let quests pile up — finish before starting new ones
