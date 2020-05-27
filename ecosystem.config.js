module.exports = {
  apps: [
    {
      name: "habitsstreak",
      script: "habitsstreak.py",
      interpreter: "pipenv",
      interpreter_args: "run python",
    },
    {
      name: "habitsstreak-cyri",
      script: "habitsstreak-cyri.py",
      interpreter: "pipenv",
      interpreter_args: "run python",
    },
    // {
    //   name: "testyo",
    //   script: "test.py",
    //   interpreter: "pipenv",
    //   cron_restart: "* * * * *",
		// 	interpreter_args: "run python",
		// 	autorestart: false
    // },
  ],
};
