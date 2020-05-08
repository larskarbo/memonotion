module.exports = {
  apps : [{
    name: 'habitsstreak',
    script: 'habitsstreak.py',
    interpreter : "pipenv",
    interpreter_args: "run python"
  }
  // ,{
  //   name: 'habitsstreakcyri',
  //   script: 'habitsstreak-cyri.py',
  //   interpreter : ".venv/bin/python",
  // }
],
};
