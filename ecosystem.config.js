const defaults = {
	time: true
}

const pipenv = {
	interpreter: "pipenv",
	interpreter_args: "run python",
	...defaults
}

module.exports = {
  apps: [
    {
      name: "habitsstreak",
			script: "habitsstreak.py",
			...pipenv
    },
    {
      name: "habitsstreak-cyri",
			script: "habitsstreak-cyri.py",
			...pipenv
    },
  ],
};
