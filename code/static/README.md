
**Static Files:**

Static files are used to serve assets such as CSS stylesheets, JavaScript files, images, fonts, and other resources that do not change dynamically based on user interactions or data. Here's why we need static files:

- **Efficient Resource Loading:** Static files are served directly by the web server (e.g., Nginx or Apache) without involving the Flask application. This makes resource loading more efficient and reduces the load on the application server.

- **Caching:** Static files can be cached by web browsers, allowing them to be stored locally on users' devices. This improves page loading times and reduces bandwidth usage.

- **Separation of Concerns:** Separating static assets from dynamic content (handled by templates) follows the principle of separation of concerns. It makes the codebase cleaner and more maintainable.

- **Optimization:** Developers can optimize and minify static files for performance. For example, CSS and JavaScript files can be minified to reduce their size and improve load times.
