export function handle(x: number, y: number, z: number, a: number) {
  let someVariable = 0;
  if (x === y) someVariable = 1;
  if (x > 0) {
    doSomething();
  }
  if (z === a) {
    doSomethingElse();
  }
  return someVariable;
}
