# Summary of DAY1 discussion - breaking down "Generation of Synthetic HTS data with artifical features"

![whiteboard-image](Day1-Whiteboard.HEIC "Whiteboard State")


The left hand side of the whiteboard image describes the fully-composed set of operations to go from a reference genome
to simulated reads. The steps, and associated work, are as follows:

1. Modification of reference, either with specific edits, or parameterised to inject N edits of type T (e.g. SNP, Del, Ins) with appropriate distributions with respect to e.g. size, position, etc.
  - It's expected that this tool will be used on small subsections of the genome, rather than injecting across entire genomes.
    For example, you might be intending to test a function over deletions in a known low-complexity 5000bp strech of the reference
  - By injecting edits onto the reference, you're simulating "samples" - biological entities which truly differ from the reference genome in some
    quantifiable way. If you then simulate sequence data from that mutated reference, you can test over data in which your desired edit may be obscured
    by sequencing noise and so on. Useful for aligners, variant callers, etc.

2. Generating sequence data from ref using models (e.g. platform-specific, tissue-specific, sample-specific). This is a well-trodden ground, but exposing it via an API for testing against small chunks of reference is useful and novel, even without injecting artificial features and edits.
  - Looking at NEAT, ART, wgsim as sources of inspiration, model parameters, and quite possibly code.

3. Post-simulation edit insertion - similar to step 1, except on reads rather than reference. By example, say you want to insert 3 randomly distributed deletions with an associated dip in quality on every read, or alternately generate 100 reads from an initial read which each have 3 of these deletions. This would look like a series of edit functions/objects which can be composed, and some kind of validity/constraint satisfaction checker that the read is both valid and fulfills the user request

4. Interfaces. For this tool to be useful we need ergonomic and convenient interfaces for the user such that they can easily use this test data over a given function or process. For now the inclination is to focus on dev-side testing frameworks such as pytest - so the question is how are we going to plug in steps 1, 2, and 3 to pytest so it can run over that data.
  - We're looking at Faker, which allows definition of custom providers that can plug straight into pytest and other frameworks
