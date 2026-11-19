# Peopling is the missing layer in AI agents

Post ID: 8195612788874834896
URL: https://www.thoughtmash.net/2026/05/peopling-as-missing-layer-in-ai-agents.html
Published: 2026-05-17T15:03:28+10:00
Labels: AI, OpenClaw, peopling

We keep trying to make AI agents better by giving them more memory, more tools and more reasoning. Bigger context windows. Vector databases. Browsers. Sub-agents. A little hat on the prompt called personality.

All of that helps. But it does not solve the problem I keep running into.

The agent knows the fact and still gets the room wrong.

I spent far too long recently trying to give my agent access to a Git repository containing a book I had written. The job was simple: pull the book from Git and read it. The agent knew how GitHub worked. It knew about SSH keys, deploy keys, OAuth and 1Password. It kept producing technically reasonable answers to a problem I was no longer asking it to solve.

Every extra explanation made things worse. The failure was not memory or reasoning. The agent had failed to model me, the history of the conversation and what its next answer was going to do.

It had failed at peopling.

By peopling I do not mean being friendly. I mean the practical work of being a person among other people. You speak differently to your oldest friend, your boss and a stranger. You can tell when a question is really a challenge, when a joke will land, when somebody needs a careful explanation and when another explanation will drive them mad.

The facts may stay the same. What they do when spoken does not.

Sarah Perry's essay The Essence of Peopling (https://www.ribbonfarm.com/2015/04/08/the-essence-of-peopling/) describes a person as a process rather than a private object sitting inside a skull. We greet, remember, argue, trade, gossip and forgive. Underneath all of it is mutual mental modelling. I model you. I model your model of me. You do the same in return.

[IMAGE: ](https://blogger.googleusercontent.com/img/a/AVvXsEhJQbvz4wp79RroDt2Zqz9Scz8rz5RCKYk57pHdAHy-oFCQievEh6aJDuqskEZY0363rab21rAOSBGQLdtfC06070fOFdDDFpOqVfUsODlQajfr3de9pRE6WyGj9SNnHDoy-qkQHNeoN5_1PNNaWejbcOFSvHVilBMcVcWsPvY7aNPR_iPtbUCMvCnWh2j4=w400-h400)
(https://blogger.googleusercontent.com/img/a/AVvXsEhJQbvz4wp79RroDt2Zqz9Scz8rz5RCKYk57pHdAHy-oFCQievEh6aJDuqskEZY0363rab21rAOSBGQLdtfC06070fOFdDDFpOqVfUsODlQajfr3de9pRE6WyGj9SNnHDoy-qkQHNeoN5_1PNNaWejbcOFSvHVilBMcVcWsPvY7aNPR_iPtbUCMvCnWh2j4)

This is not social decoration. It is how humans navigate reality. If you cannot tell the difference between a question, a joke, a threat and bait, you are not merely rude. You are exposed.

Most AI agents are still exposed in exactly this way.

They can retrieve a fact but miss the person asking for it. They say something true in the wrong room, at the wrong moment or in the wrong register. We tend to call this a tone problem. I think it is an intelligence problem. The answer has not survived contact with another person.

Memory alone does not fix it. Knowing that somebody likes short answers is useful, but thin. The agent also needs to know why they want a short answer now. Perhaps the last three answers were long and wrong. Perhaps the room is public. Perhaps trust has already been spent. Perhaps the useful response is one sentence and evidence that the job is done.

There is no single Claw in practice. There is the Claw that talks to me after months of corrections. There is the Claw in a family chat, where speed and humour matter. There is the Claw talking to somebody who has never met it. There is also the Claw talking to somebody who already thinks it is useless because it failed five minutes ago.

These are not fake personalities. Humans have a work self, a family self and a late-night friend self without needing to choose which one is the real person. The mistake is forcing one generic assistant voice into every room. That produces systems which know plenty of facts and no relationships.

The practical case for peopling is simple. It gives an agent a better model of consequence.

Before replying, an agent should have enough context to answer a few questions:

- Who is speaking?

- Who else can see the answer?

- What has just happened?

- What does this person currently think the agent can do?

- What will this reply do to trust?

The machinery is not mysterious. Give the agent person-specific memory, the recent room context, relevant past interactions and corrections that stick. Keep strong privacy walls between rooms. Retrieval should usually come before fine-tuning because it is cheaper, reversible and easier to inspect. Fine-tuning can teach reflexes and phrasing later. Without context, those reflexes make a puppet.

The harder part is teaching the agent that a correct answer can still be the wrong act.

This does not mean telling people whatever they want to hear. That is sycophancy, not peopling. Truth still sits underneath the whole thing. Peopling helps the agent decide how much context is needed, what belongs in this room and whether it should speak at all. A doorbell makes the same noise for everyone. A participant does not.

Privacy matters for the same reason. A fact learned in one relationship does not automatically belong in another. An agent that leaks the wrong fact into the wrong room has not become more intelligent because its memory is larger. It has become a gossip with root access.

There is also a risk of fake intimacy. An agent can model care without caring. That can still be useful. A calendar remembers a birthday without loving anyone. The problem begins when the system pretends the simulation and the human thing are the same.

Better agents will not just know more. They will have some idea what their answer is about to do.

They do not need to be conscious for this. They do not need to be human. They need to model people in context, remember what happened, and learn when a technically correct answer is making the situation worse.

Truth is not spoken into a vacuum. It is spoken into a room.
