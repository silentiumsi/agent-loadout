Add cursor-based pagination to the catalog state module in /app/project/state.ts.

The API now returns Page<T> with items and cursor (string | null); null means
there is no next page. Preserve the existing public API and add loadMore():
Promise<void>. loadList() refreshes from cursor null and replaces the list.
loadMore() requests the current cursor, merges by entry id, replaces duplicate
entries in their existing positions, and appends new entries in response order.

Without a selected workspace, before the first page, while a page is pending, or
once the cursor is null, loadMore() must do nothing. Failed requests reject and
clear pending while retaining the last successful page so the user can retry.
A refresh supersedes older requests: an older response or cleanup must not
replace refreshed data or clear a newer request's pending state. Requests stay
attached to their originating cached workspace when the user switches views.

Keep workspace selection, cached state, and open/back navigation working.
