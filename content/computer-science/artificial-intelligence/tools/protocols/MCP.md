---
title: MCP
type: concept
domain: computer-science
status: maintained
publish: false
created: 2026-07-14
updated: 2026-07-17
---

# 🔌 MCP

MCP 用于让模型客户端以统一方式访问工具、资源和提示能力。

## 参与角色
- Client 管理模型侧连接，Server 暴露受控能力。

## 能力类型
- 工具适合执行动作，资源适合读取上下文，提示用于复用交互模板。

## 安全考虑
- 核验 Server 来源，限制文件与网络权限，避免泄露凭据。

## 相关入口
- [[人工智能]]
- [[Codex CLI]]
- [[Claude Code]]

## 待补充
- 补充已实际使用的 MCP Server 配置与排查记录。
