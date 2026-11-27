# Lifecycle hygiene

A long-running service
fails in ways a request handler does not.
A background task dies and the process keeps running,
a database goes down for maintenance and the workers never recover,
a probe reports healthy while nothing is being processed.
These failures stay invisible in tests and surface in production.

- A background task never dies silently.
  When it fails,
  it restarts with backoff
  or takes the service down.
  Decide which, per task.
- A dependency outage pauses work with backoff,
  and the service resumes on its own once the dependency is back.
  No manual restart.
- Readiness reflects whether the service can do its actual job,
  including the dependencies and tasks that job needs.
  A listening port or a metrics endpoint
  is not proof of that.
- Start prerequisites before accepting work,
  and keep liveness distinct from readiness.
  Withdraw readiness as soon as shutdown begins;
  prevent an in-flight startup from marking it ready again.
  A startup-complete check alone is not ongoing health monitoring.
- Shutdown is idempotent
  and releases every resource the service opened:
  tasks, consumers, clients, and connections.
- Give every task and resource one lifecycle owner,
  including resources allocated before startup fails or is cancelled.
  Stop accepting work before its dependencies,
  use a bounded overall shutdown budget,
  and report incomplete cleanup rather than claiming it succeeded.
  Cancellation and cleanup failures must not silently hide the original failure.
