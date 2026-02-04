#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

async function main() {
  const shouldPublish = process.argv.includes("--publish");
  const rootDir = path.resolve(__dirname, "..");
  const mappingPath = path.join(rootDir, "codex", "collaboration", "notion-relay.json");

  const maxPages = parseInt(process.env.NOTION_RELAY_MAX_PAGES || "10", 10);
  const token = process.env.NOTION_TOKEN || "";
  const heartbeatDb = process.env.NOTION_DB_HEARTBEAT_ID || "";
  const finDb = process.env.NOTION_DB_FINANCIAL_MODELS_ID || "";
  const clientDb = process.env.NOTION_DB_CLIENT_CONFIGS_ID || "";

  /** Safe no-op when secrets missing */
  const canPublish = Boolean(token);

  const exists = fs.existsSync(mappingPath);
  if (!exists) {
    console.error(`[notion-relay] mapping file missing: ${mappingPath}`);
    process.exit(2);
  }

  const mapping = JSON.parse(fs.readFileSync(mappingPath, "utf8"));

  const plan = [];

  function addPlan(kind, dbId, items) {
    if (!Array.isArray(items) || items.length === 0) return;
    const limited = items.slice(0, maxPages);
    plan.push({ kind, dbId, count: limited.length });
  }

  addPlan("heartbeat", heartbeatDb, mapping.heartbeat?.items || []);
  addPlan("financial_models", finDb, mapping.financial_models?.items || []);
  addPlan("client_configs", clientDb, mapping.client_configs?.items || []);

  if (!shouldPublish) {
    console.log(JSON.stringify({ mode: "plan", canPublish, maxPages, plan }, null, 2));
    return;
  }

  if (!canPublish) {
    console.log(JSON.stringify({ mode: "publish", skipped: true, reason: "missing NOTION_TOKEN", plan }, null, 2));
    return;
  }

  const { Client } = require("@notionhq/client");
  const notion = new Client({ auth: token });

  async function publishGroup(kind, dbId, schema, items) {
    if (!dbId) return { kind, dbId, published: 0, skipped: items.length, reason: "missing database id" };
    const limited = items.slice(0, maxPages);
    let published = 0;
    for (const item of limited) {
      const properties = buildPropertiesFromSchema(schema, item);
      try {
        await notion.pages.create({ parent: { database_id: dbId }, properties });
        published += 1;
      } catch (err) {
        console.error(`[notion-relay] Failed to publish item to ${kind}:`, item, err);
        // continue on error, report summary only
      }
    }
    return { kind, dbId, published, attempted: limited.length };
  }

  function buildPropertiesFromSchema(schema, item) {
    const properties = {};
    for (const [propName, spec] of Object.entries(schema || {})) {
      const type = spec.type;
      const val = item[propName];
      if (type === "title") {
        properties[propName] = { title: [{ type: "text", text: { content: String(val ?? "") } }] };
      } else if (type === "rich_text") {
        properties[propName] = { rich_text: [{ type: "text", text: { content: String(val ?? "") } }] };
      } else if (type === "number") {
        properties[propName] = { number: typeof val === "number" ? val : Number(val ?? 0) };
      } else if (type === "select") {
        if (val == null || val === "") continue;
        properties[propName] = { select: { name: String(val) } };
      } else if (type === "multi_select") {
        const arr = Array.isArray(val) ? val : (val !== null && val !== undefined ? [val] : []);
        properties[propName] = { multi_select: arr.map((x) => ({ name: String(x) })) };
      } else if (type === "created_time") {
        // Notion ignores created_time on create; skip to avoid errors
        continue;
      }
    }
    return properties;
  }

  const results = [];
  if (mapping.heartbeat?.items?.length) {
    results.push(await publishGroup("heartbeat", heartbeatDb, mapping.heartbeat.schema_mapping, mapping.heartbeat.items));
  }
  if (mapping.financial_models?.items?.length) {
    results.push(await publishGroup("financial_models", finDb, mapping.financial_models.schema_mapping, mapping.financial_models.items));
  }
  if (mapping.client_configs?.items?.length) {
    results.push(await publishGroup("client_configs", clientDb, mapping.client_configs.schema_mapping, mapping.client_configs.items));
  }

  console.log(JSON.stringify({ mode: "publish", canPublish, maxPages, results }, null, 2));
}

main().catch((err) => {
  console.error("[notion-relay] fatal", err);
  process.exit(1);
});

