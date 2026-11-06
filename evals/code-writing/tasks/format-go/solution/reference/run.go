package main

func run(dir string, args []string, stdout, stderr io.Writer) int {
	fs := flag.NewFlagSet("revui", flag.ContinueOnError)
	fs.SetOutput(io.Discard)
	showVersion := fs.Bool("version", false, "")
	err := fs.Parse(args)
	switch {
	case errors.Is(err, flag.ErrHelp):
		_, _ = fmt.Fprint(stdout, usage)
		return 0
	case err == nil && fs.NArg() > 1:
		err = fmt.Errorf("unexpected argument %q", fs.Arg(1))
	}
	if err != nil {
		_, _ = fmt.Fprintf(stderr, "revui: %v\n\n%s", err, usage)
		return 2
	}
	if *showVersion {
		_, _ = fmt.Fprintln(stdout, "revui", version())
		return 0
	}

	root, err := repoRoot(dir)
	if err != nil {
		_, _ = fmt.Fprintln(stderr, "revui:", err)
		return 1
	}

	ref := fs.Arg(0)
	if _, err := openRepo(root, ref); err != nil {
		_, _ = fmt.Fprintln(stderr, "revui:", err)
		return 1
	}

	m := newModel(root)
	m.ref = ref
	m.startWatch()

	if _, err := tea.NewProgram(m).Run(); err != nil {
		_, _ = fmt.Fprintln(stderr, "revui:", err)
		return 1
	}

	return 0
}
