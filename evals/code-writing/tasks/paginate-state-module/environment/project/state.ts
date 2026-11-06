export interface Page<T> {
  items: T[];
}
export interface Entry {
  id: string;
  title: string;
}
export interface Section<T> {
  data?: T;
  pending: boolean;
  generation: number;
}
export interface WorkspaceState {
  key: string;
  selected: string | null;
  list: Section<Page<Entry>>;
}
const section = <T>(): Section<T> => {
  return { pending: false, generation: 0 };
};
export class CatalogState {
  current?: WorkspaceState;
  private readonly workspaces = new Map<string, WorkspaceState>();
  constructor(private readonly fetchPage: (key: string, cursor: string | null) => Promise<Page<Entry>>) {}
  select(key: string): void {
    let state = this.workspaces.get(key);
    if (!state) {
      state = { key, selected: null, list: section() };
      this.workspaces.set(key, state);
    }
    this.current = state;
  }
  cached(): readonly WorkspaceState[] {
    return [...this.workspaces.values()];
  }
  open(id: string): void {
    const state = this.current;
    if (!state) return;
    state.selected = id;
  }
  back(): void {
    if (this.current) this.current.selected = null;
  }
  async loadList(): Promise<void> {
    const state = this.current;
    if (!state) return;
    const target = state.list;
    const generation = ++target.generation;
    target.pending = true;
    try {
      const next = await this.fetchPage(state.key, null);
      if (target.generation !== generation) return;
      target.data = next;
    } finally {
      if (target.generation === generation) target.pending = false;
    }
  }
}
