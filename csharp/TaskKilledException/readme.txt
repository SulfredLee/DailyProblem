Aim
    - This is an example to repeat the task cancel exception and trying to solve it.
Background
    - When we are doing WPF gui application, we may use dispatcher.invoke() to update UI related components.
    - If we shutdown the application by Application.Current.Shutdown(), there is a chance that the task cancel exception pop up due to the running of the message loop.
Solution
    - Use Environment.Exit(0) to shutdown the application
