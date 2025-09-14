from py_hts_synth import Ref, FragmentSynth, IlluminaModel, BloodQualModel, Constraint, Edit

ref = Ref.from_fasta("ref.fa")
loc = ref.locus("chr1", 1000, 2000)  # reference slice


gen = FragmentSynth.Generator(
    # ~an API to simulate sequence data~
    locus=loc,
    layout=FragmentSynth.Layout(
        r1_len=150,
        r2_len=150,
        frag_orientations="FR",  # e.g. r1 forward, r2 reverse
        insert_size_mean=100,
        insert_size_sd=20,
        ...,  # more parameters describing fragment format
    ),
    profile=IlluminaModel(  # probably something we'd ship since it's generic to a platform
        seed=42,
        qual_model=BloodQualModel01(qual_range=(10, 38)),  # soemthing we might provide an interface for the user to create rather than pre ship
        sub_rate=0.001,
        ins_rate=0.0001,
        del_rate=0.0001,
        ...  # and so on
    ),
    # ~and apply constraints to that data~
    # (one possible example)
    # fragment fulfills ~one or both~ properties:
    # At least one and at most 2 3bp deletions present in forward read of fragment
    # One transversion in both reads
    fragment_constraints=Constraints.Any(
        FragmentSynth.EditEvent(Edit.Del(size=3), count=(1, 2), on_read='r1'),
        FragmentSynth.EditEvent(Edit.Snv(type='transversion'), count=1, on_read='both')
    ),
    # TODO:
    # apply events to an imaginary "sample" of the given reference,
    # prior to simulating sequence data (reads) from that sample
    # (rather than/in addition to injecting events directly onto reads post-simulation, as above)
    sample_constraints=...
)


# now you have a generator that will return Fragment objects
reads = gen.emit_reads(n=100)


# and then test over some function
