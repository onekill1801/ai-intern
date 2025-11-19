// worker.ts
import { NativeConnection, Worker } from '@temporalio/worker';
import * as activities from './activities';

async function run() {
  console.log("🚀 Worker starting...");

  const connection = await NativeConnection.connect({
    address: 'localhost:7233',
  });

  console.log("🔌 Connected to Temporal");

  // 🟢 Wrap activities để log khi gọi
  const loggedActivities: any = {};
  for (const key of Object.keys(activities)) {
    loggedActivities[key] = async (...args: any[]) => {
      console.log(`🔧 [Activity Start] ${key}(${JSON.stringify(args)})`);
      const result = await (activities as any)[key](...args);
      console.log(`✅ [Activity Done] ${key} → ${JSON.stringify(result)}`);
      return result;
    };
  }

  const worker = await Worker.create({
    connection,
    namespace: 'default',
    taskQueue: 'hello-world',
    workflowsPath: require.resolve('./workflows'),
    activities: loggedActivities,
  });

  console.log("👂 Worker listening on taskQueue: hello-world");

  await worker.run();
}

run().catch((err) => {
  console.error("Worker error:", err);
  process.exit(1);
});
