import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import * as ExternalPlugin from "./.quartz/plugins"
import type { ExplorerOptions } from "./.quartz/plugins"

const mapExplorerNode: ExplorerOptions["mapFn"] = (node) => {
  const folderNames: Record<string, string> = {
    "computer-science": "计算机科学",
    "algorithms-and-data-structures": "算法与数据结构",
    "programming-languages": "编程语言",
    go: "Go",
    python: "Python",
    systems: "计算机系统",
    networking: "计算机网络",
    "operating-systems": "操作系统",
    "software-engineering": "软件工程",
    backend: "后端开发",
    devops: "DevOps",
    "version-control": "版本控制",
    "artificial-intelligence": "人工智能",
    "computer-vision": "计算机视觉",
    "visual-localization": "视觉定位",
    tools: "AI 工具与实践",
    agents: "Agent 与编码工具",
    prompting: "提示词工程",
    protocols: "工具协议",
    workflows: "AI 工作流",
    resources: "研究资料",
    datasets: "数据集与基准",
    metrics: "评价指标",
    papers: "论文",
    references: "参考资料",
    collections: "资源收藏",
    commands: "命令速查",
    glossary: "术语表",
    surveys: "综述与报告",
    practice: "实践记录",
    decisions: "技术决策",
    experiments: "实验记录",
    projects: "项目记录",
    troubleshooting: "问题排查",
    writing: "写作与输出",
    academic: "学术写作",
    reference: "内部规范",
    checklists: "检查清单与规范",
  }
  const overviewPages = new Set([
    "computer-science/计算机科学",
    "computer-science/algorithms-and-data-structures/算法与数据结构",
    "computer-science/programming-languages/编程语言",
    "computer-science/programming-languages/go/Go语言",
    "computer-science/programming-languages/python/Python语言",
    "computer-science/systems/计算机系统",
    "computer-science/systems/networking/计算机网络",
    "computer-science/software-engineering/软件工程",
    "computer-science/software-engineering/backend/后端开发",
    "computer-science/artificial-intelligence/人工智能",
    "computer-science/artificial-intelligence/computer-vision/计算机视觉",
    "computer-science/artificial-intelligence/computer-vision/visual-localization/视觉定位",
    "computer-science/artificial-intelligence/tools/prompting/提示词工程",
    "resources/研究资料",
    "resources/datasets/数据集与基准",
    "resources/metrics/评价指标",
    "resources/papers/论文",
    "resources/references/参考资料",
    "resources/references/collections/资源收藏",
    "resources/references/commands/命令速查",
    "resources/references/glossary/术语表",
    "resources/surveys/综述与报告",
    "practice/实践记录",
    "practice/decisions/技术决策",
    "practice/experiments/实验记录",
    "practice/projects/项目记录",
    "practice/troubleshooting/问题排查",
    "writing/写作与输出",
    "writing/academic/学术写作",
  ])

  if (node.isFolder && node.slugSegment) {
    node.displayName = folderNames[node.slugSegment] ?? node.displayName
  } else {
    const slug = (node.data as { slug?: string } | null)?.slug
    if (slug && overviewPages.has(slug)) {
      node.displayName = "概览"
    }
  }
  return node
}

const sortExplorerNodes: ExplorerOptions["sortFn"] = (a, b) => {
  const aOverview = a.displayName === "概览"
  const bOverview = b.displayName === "概览"
  if (aOverview !== bOverview) return aOverview ? -1 : 1
  if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
  return (a.displayName ?? "").localeCompare(b.displayName ?? "", "zh-CN", {
    numeric: true,
    sensitivity: "base",
  })
}

ExternalPlugin.Explorer({
  mapFn: mapExplorerNode,
  sortFn: sortExplorerNodes,
  order: ["filter", "map", "sort"],
})

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
