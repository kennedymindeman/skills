# Chat: stacked branch broke after squash-merge

**User:** I had feature-b stacked on feature-a. feature-a got squash-merged into main, and now the PR for feature-b shows all of feature-a's commits again plus a pile of conflicts. What happened?

**Assistant:** A squash-merge writes one brand-new commit on main. It has the same content as feature-a's commits, but different commit IDs. Git compares branches by commit ID, not by content. So from feature-b's point of view, none of feature-a's original commits are on main yet.

**User:** So the merge base is the problem?

**Assistant:** Yes. The merge base of main and feature-b is still the commit where feature-a branched off main. Everything after that point on feature-b, including feature-a's old commits, counts as "new" relative to main. That is why the PR diff shows them again, and why replaying them conflicts with the squashed copy.

**User:** How do I fix it without redoing my work?

**Assistant:** Replay only the commits that are unique to feature-b, and put them on top of main:

    git rebase --onto main feature-a feature-b

Read it as: take the commits in feature-b that are not in feature-a, and replay them onto main. feature-a here is your local, pre-squash branch, which still points at the old commits. After the rebase, force-push feature-b with `git push --force-with-lease`.

**User:** That worked. The PR now shows only my two commits.

**Assistant:** Good. Next time, run the rebase right after the parent PR lands, before you delete feature-a locally. Without the old feature-a ref you would have to find that commit ID in the reflog.
