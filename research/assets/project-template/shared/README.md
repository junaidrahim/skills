# Shared Libraries

Use immutable version directories such as `python/v001` or `rust/v001`. A frozen experiment declares the exact versions it uses in `experiment.toml`.

Never edit a shared version used by a frozen experiment. Copy it to the next version.
