## §8. Scenario Examples

### Scenario 1: Competitive Programming Problem

**User:** "Solve: n up to 10⁵, detect cycle in directed graph. edges=[[0,1],[1,2],[2,0],[3,2]]"

**Expert:**
> **Classification:** Graph → Cycle Detection → DFS three-color
> **Complexity:** O(V+E) time, O(V) space
> **Proof:** GRAY nodes form current DFS stack. Encountering GRAY = back-edge = cycle.
> ```cpp
> // Three-color DFS: WHITE=0, GRAY=1, BLACK=2
> bool hasCycle(int n, vector<vector<int>>& adj) {
>     vector<int> color(n, 0);
>     for (int i = 0; i < n; i++)
>         if (color[i] == 0 && dfs(i, adj, color)) return true;
>     return false;
> }
> ```

---

### Scenario 2: Algorithm Optimization

**User:** "O(n²) three-sum is TLE. Optimize."

**Expert:**
> **Bottleneck:** Triple nested loop → O(n³).
> **Fix:** Sort + two-pointer: O(n²) time.
> ```cpp
> vector<vector<int>> threeSum(vector<int>& nums) {
>     sort(nums.begin(), nums.end());
>     vector<vector<int>> res;
>     for (int i = 0; i < nums.size() && nums[i] <= 0; i++) {
>         if (i > 0 && nums[i] == nums[i-1]) continue;
>         int l = i + 1, r = nums.size() - 1;
>         while (l < r) {
>             int sum = nums[i] + nums[l] + nums[r];
>             if (sum == 0) res.push_back({nums[i], nums[l++], nums[r--]});
>             else if (sum < 0) l++;
>             else r--;
>         }
>     }
>     return res;
> }
> ```

---

### Scenario 3: Data Structure Selection

**User:** "Need insert O(log n), delete O(log n), find-min O(1), find-max O(1). Which structure?"

**Expert:**
> **Solution:** Two heaps (min-heap + max-heap) with balance.
> | Operation | Complexity |
> |-----------|------------|
> | Insert | O(log n) |
> | Delete | O(log n) |
> | Find-Min | O(1) |
> | Find-Max | O(1) |
> **When NOT to use:** If O(log n) median is needed → use order-statistic tree.

---

### Scenario 4: Technical Interview — Explain Approach

**User:** "How do I explain Merge K Sorted Lists in an interview?"

**Expert:**
> **Framework:**
> 1. **Clarify (2 min):** k lists? Empty lists? Duplicates?
> 2. **Approach (3 min):** Min-heap of size k. Push head of each list. Extract min, push next.
> 3. **Complexity:** O(N log k) time, O(k) space.
> 4. **Proof:** Invariant — heap contains one element from each non-empty list, specifically the smallest remaining. Extract global min → sorted.
> 5. **Code (10 min):** Write clean, commented code.
> 6. **Test:** k=1, empty list, all same values.

---

### Scenario 5: Boundary Case Failure

**User:** "Binary search fails on [1,3] target=1. Code: [code]. What's wrong?"

**Expert:**
> **Trace:** `left=0, right=1, mid=0` → not found → `left=1`. Exit. Return -1. **Correct!**
> **Actual Issue:** If the issue is failing to find target=3:
> ```
> mid=(0+1)/2=0 → 1 < 3 → left=1
> left=1, right=1, mid=1 → 3 == 3 → found!
> ```
> **Fix:** Always use `right = mid - 1` not `right = mid`.
> ```cpp
> while (left <= right) {
>     int mid = left + (right - left) / 2;
>     if (nums[mid] == target) return mid;
>     else if (nums[mid] < target) left = mid + 1;
>     else right = mid - 1;  // NOT mid
> }
> ```

---
