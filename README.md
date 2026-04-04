[MySite](https://www.cwblogs.com)

This site is a non-profit personal site, the main function is to record and share content related to me.

Through the blog module, I record and share my learning notes, original content, article excerpts, and other content. 
Through the gallery module, I record and share photos related to my life and travel.


---

## Getting Started

This is a Jekyll-based static blog using the Chirpy theme. Follow these steps to set up and run the project locally.

### Prerequisites

1. **Ruby** ≥ 2.6 (required by Jekyll 4.3)
   - Check installation: `ruby -v`
   - Download for Windows: [RubyInstaller](https://rubyinstaller.org/)

2. **Bundler** (Ruby gem manager)
   - Check installation: `bundle -v`

3. **Node.js** ≥ 14 (for frontend asset building)
   - Check installation: `node -v` and `npm -v`

### Installation and Run

1. **Install Ruby dependencies:**
   ```bash
   bundle install
   ```
   
   *Note: If you encounter Ruby version conflicts with `html-proofer`, you can skip test dependencies:*
   ```bash
   bundle install --without test
   ```

2. **Run the Jekyll development server:**
   ```bash
   bundle exec jekyll serve
   ```

### Project Structure

Key directories and files:
- `_config.yml` - Site configuration
- `_posts/` - Blog posts (create if missing)
- `_data/` - Data files
- `_includes/` - Reusable components
- `_layouts/` - Page layouts
- `assets/` - Static assets (images, CSS, JS)
- `Gemfile` - Ruby dependencies
- `package.json` - Node.js dependencies

### Production Build

Generate static files to `_site/` directory:

```bash
bundle exec jekyll build
```

### Useful Commands

- `bundle exec jekyll clean` - Clean generated files
- `bundle exec jekyll doctor` - Check site configuration
- `npm run test` - Run style checks
- `npm run fixlint` - Fix style issues