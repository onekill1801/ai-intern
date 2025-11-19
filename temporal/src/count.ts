import { Connection, TaskQueue } from '@temporalio/client';

const connection = await Connection.connect();
const client = new WorkflowClient({ connection });

const tqInfo = await client.taskQueues.describe('hello-queue');

console.log(tqInfo.pollers.length);
