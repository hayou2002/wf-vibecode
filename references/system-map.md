# wf-vibecode 体系图

这条工作流不是一个大而全的技能，而是「一层壳 + 一组零件 + 一份项目契约」。升级零件或换宿主时，先看这张图，知道该动哪一层。

## 四层

| 层 | 放什么 | 谁维护 |
| --- | --- | --- |
| 0 路由 | 全局 `AGENTS.md` 里的 `wf-router` 段：命中场景就先读对应工作流 | wf-maker 生成，人工确认 |
| 1 工作流 | `wf-vibecode`、`wf-design`、`wf-github-ops`、`wf-newapi-manager`、`wf-maker` | 每个 wf- 自己 |
| 2 零件 | `oil-explore`、`oil-plan`、`oil-delegate`、`oil-code-review`、`oil-bug-fix`、`oil-govern`、`oil-frontend`、`vibehub`、`webapp-testing`、`git-ship` | 上游仓库 + magpie |
| 3 项目契约 | 项目 `AGENTS.md` 的 `oil-dev` 小节、`docs/术语表.md`、`docs/` 方案 | 项目自己 |
| 4 宿主能力 | Codex 原生子 Agent、shell、真实浏览器 | 宿主提供 |

## 一次改动怎么流

```text
需求
  → 路由层选工作流
  → 定档(T0 / T1 / T2 / 故障 / 收口 / 治理)
  → 零件层按需取用(不全走)
  → 项目契约提供快测、门禁、高风险与禁改目录
  → 分层验证(秒级 → 关联快测 → 合并门禁)
  → 收口:说清改了什么、验证了什么、没做什么
```

## 谁负责什么

| 事情 | 交给谁 | 不交给谁 |
| --- | --- | --- |
| 只读摸清调用链、找可复用组件 | `oil-explore` + 宿主只读子 Agent | 主 Agent 从头读十几个大文件 |
| 写人看得懂的方案、定验收点 | `oil-plan` | 直接开写 |
| 把任务交给另一个 CLI | `oil-delegate`(已配好 runner 时) | 默认动作 |
| 审代码、查越界与高风险 | `oil-code-review` | 让写代码的同一上下文自审 |
| 原因不明的缺陷 | `oil-bug-fix` | 在报错处加兜底 |
| 文档、测试、worktree、分支治理 | `oil-govern` | 凭印象手动整理 |
| 签名、打包、发版 | 项目自己的脚本 | 这套技能 |

## 委派与子 Agent

- 先看宿主:Codex 用原生子 Agent,Claude 用 Task;只读任务优先拆出去,只回简报。
- 跨 CLI 才用 `oil-delegate`;先在它那里 onboarding 选 runner。本机只探测到 `dsh`。
- 写代码的任务:工作区干净或独立 worktree;审查、会诊只读,回来核对 `git status`。
- 任务描述会发给外部模型,可能计费;不放密钥和隐私数据。
- 个人偏好写 `~/.oil-dev/preferences.md`,按宿主分节;写角色不写型号。

## 升级后的接线清单

1. 用 magpie 更新技能,或把上游 `skills/<name>` 覆盖到 `~/.config/magpie/library/skills/<name>`。
2. 跑技能自带测试:`python -m unittest discover -s <skill>/tests -p "test_*.py"`。
3. 重新登记依赖,让 `sources.json` 的摘要更新:`python wf.py link wf-vibecode <skill> --mode reference --uses "..."`。
4. 刷新环境清单:`python wf.py env wf-vibecode`。
5. 校验工作流:`python wf.py check wf-vibecode` 和 `python wf.py validate wf-vibecode`。
6. 用一个真实小任务走一遍,确认路由、车道和验证都接得上。

## 已知缺口

- `oil-delegate` 在本机只探测到 `dsh`;要委派给 Codex 或 Claude,得先装对应 CLI 并配置 runner。Codex 内优先用原生子 Agent。
- `oil-delegate` 的单元测试在 Windows 上因 POSIX 测试桩失败;扫描和调用逻辑可用,但升级后要手动确认一次。
- 定时治理还没装成自动化;`oil-govern` 支持每日巡检,但默认只报告,不自动删改。
## 维护备注

- 这五个技能是手动覆盖 magpie 库文件升级的,`library.json` 里的哈希还没重算;以后 `magpie library skill update` 会把它们当成「本地改动」跳过,要更新得用 `--replace-edits`。

