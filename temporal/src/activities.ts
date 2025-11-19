// activities.ts
export async function greet(name: string): Promise<string> {
  console.log(`🔧 Activity greet() started for: ${name}`);

  // sleep 15 giây
  await new Promise(resolve => setTimeout(resolve, 15000));

  console.log(`✅ Activity greet() finished for: ${name}`);
  return `Hello, ${name}!`;
}
