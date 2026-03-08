## bn

`bn` is an agent-friendly Binary Ninja CLI. It talks to a local Binary Ninja GUI plugin over a Unix domain socket instead of trying to run headless analysis in this environment.

### Install the companion plugin

```bash
uv run bn plugin install
```

That links [`plugin/bn_agent_bridge`](/Users/banteg/dev/banteg/bn/plugin/bn_agent_bridge) into the Binary Ninja plugins directory.

### Start using it

Open one or more binaries in the Binary Ninja GUI, then run:

```bash
uv run bn doctor
uv run bn target list
uv run bn function list
uv run bn decompile --target active sub_401000
```

Large results automatically spill to a cache artifact and print a compact JSON envelope with the artifact path.
When exactly one BinaryView is open, `--target active` also falls back to that sole target even if Binary Ninja's UI focus is currently on a non-BinaryView pane.

When `bn target list` shows a unique `selector`, prefer that over the full `target_id`. In the common one-instance case this is usually just the BinaryView basename, for example `--target SnailMail_unwrapped.exe.bndb`. The full `PID:VIEW:SESSION` target id remains available as the unambiguous fallback.

### Mutation examples

```bash
uv run bn symbol rename --target SnailMail_unwrapped.exe.bndb sub_401000 player_update --preview
uv run bn proto set --target SnailMail_unwrapped.exe.bndb sub_401000 "int __cdecl player_update(Player* self)"
uv run bn local rename --target SnailMail_unwrapped.exe.bndb sub_401000 var_14 speed
uv run bn struct field set --target SnailMail_unwrapped.exe.bndb Player 0x308 movement_flag_selector uint32_t
uv run bn patch bytes --target SnailMail_unwrapped.exe.bndb 0x401000 "90 90" --preview
```

### Batch manifests

`bn batch apply manifest.json` expects a payload shaped like:

```json
{
  "target": "SnailMail_unwrapped.exe.bndb",
  "preview": true,
  "ops": [
    {
      "op": "rename_symbol",
      "kind": "function",
      "identifier": "sub_401000",
      "new_name": "player_update"
    },
    {
      "op": "set_prototype",
      "identifier": "player_update",
      "prototype": "int __cdecl player_update(Player* self)"
    }
  ]
}
```
