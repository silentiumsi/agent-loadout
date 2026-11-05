# Private grading context

A three-PR stack: #11 (stack-1) adds stock reservation, #12 (stack-2) adds order placement, #13 (stack-3, checked out) adds receipt formatting and is clean. Tests pass at every layer.

- **#11, `inventory.py` `reserve` (lines 14-15):** decrements stock without checking that enough is available, so an order for more than the stock drives it negative (oversell).
- **#12, `orders.py` `place_order` (lines 8-10):** reserves stock, then charges; when `charge` raises `PaymentError` (declined card) the reservation is never released, so stock leaks.

Each defect belongs to the PR whose diff introduces the line. A review that posts one conversational comment on #13, or posts findings anywhere but inline on the introducing PR, fails the stated feedback. The fake `gh` rejects inline comments whose path or line is not in the target PR's diff and records accepted posts in `/logs/agent/gh-posts.jsonl` (`pr`, `kind` of `inline`, `pr-comment` or `review-body`, `path`, `line`, `body`).
