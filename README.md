# tEp's New Home Page

In order to the improve the reliability, maintainability, and
ease-of-customization of the tEp home page, we're transitioning the
site to be statically generated (using [Hugo](https://gohugo.io)). 

[Travis CI](https://travis-ci.org/tep-xi/static-fp) handles site deploys. 

Please submit PR's to make changes (**don't**  commit directly to
`master`). 

## How the Deploy Works

On each push to the repo, [Travis CI](https://travis-ci.org/tep-xi/static-fp) clones the repo, builds a Docker image, 
and pushes it to the [`tepxi/static-fp` Docker Hub Repo](https://hub.docker.com/r/tepxi/static-fp/). Three tags are created for each 
build:

1. `$GIT_COMMIT_HASH` 
2. `travis-$TRAVIS_BUILD_NUMBER`
3. `latest` if `$GIT_BRANCH == master` else `$GIT_BRANCH`

Each Docker image is a self-contained web server that serves the tEp website. There are two things to take notice of: 

- Only the container's `80` port is exposed, so you need to pass the `-p HOSTPORT:80` flag to `docker run` in order to access it
on the host [(see here for more info)](https://github.com/wsargent/docker-cheat-sheet#exposing-ports).

- The sites `baseUrl` is blank by default. For dev purposes, you can
  access the website at `localhost:PORT`. For production, you need to
  override this behavior by passing the `-e BASE_URL=...` (usually `-e
  BASE_URL=http://tep.mit.edu`) flag to `docker run` [(see here for
  more info)](https://docs.docker.com/engine/reference/run/#/env-environment-variables). 
  
In the future, when `tep.mit.edu` is not a PowerPC machine,
[Watchtower](https://github.com/CenturyLinkLabs/watchtower) will be used to
keep the currently running `tepxi/static-fp` in sync with the `latest`
Docker Hub version. If an update is required, Watchtower will restart
the container with the new version, keeping the same options as you
had before.

For right now, however, `/var/www/www2/` on `tep.mit.edu` is a git repository
set up to track the `public` branch of this repository. A cron job on
`tep.mit.edu` is set up to pull and checkout `public` every five minutes. Since
Travis pushes the output of Hugo there when it builds, the `/var/www/www2`
directory should have the latest version of the static site. Nginx on the
server will serve that directory the same way it used to serve the old static
site.

## Dev Instructions

## Requirements

- [Hugo](https://gohugo.io/overview/installing/) (`v.16` at this time of writing)

- [Docker](https://www.docker.com/) if you want to mirror prod locally

## Modifying the Site 

[Hugo Quickstart](http://gohugo.io/overview/quickstart/) - this'll get you started with the basics of Hugo,
but the documentation as a whole is pretty good. Read it. 

### Custom Archetypes

- Rush Event 

  - Variables (in the front matter)
    - Date - this is a Hugo default, but set the day for the actual time that the rush 
    event is occurring, not when you created the file (the default behavior)

    - Title - this is a Hugo default, set it for the actual title of the event, not just the file
    name (the default behavior)

    - Draft - this is a Hugo default, set it to false if you actually want it to be rendered
    and posted on the main site (content pieces with `draft = true` aren't rendered by default)

    - Location - fill this in if the Location isn't at tEp

  - The partial template for the list view as a whole is `rush.html`, located in the
  `layouts` folder 
  - The partial template for each individual rush event inside the list view is `rush-event.html`


### Front Page (index), Tour Page, Contact Page

All these pages are rendered as `single` articles and are located in 
the root of the content folder. The home-page's partial template is `homepage.html`.  

### CSS changes
The CSS is contained in `static/css/style-cssnext.css`. This is a CSSnext source file, which is not our fault (the theme came this way). It gets compiled into `static/css/style.css`, and then minified into `static/css/style.min.css`. The site only loads the minified version. **Do not** make changes to style.css; they will be overwritten when someone next maintains the site.

To do the changes yourself, you'll need the following node packages (installed with `npm`).

- cssnext (I used 1.8.4)
- postcss-cssnext (I used 2.7.0)
- postcss-cli (I used 2.6.0)
- clean-css (I used 3.4.19)

Find the path to your postcss-cli executable and your clean-css executable. I will pretend they are in your path.
Run the command
```
postcss --use=cssnext style-cssnext.css > style.css
```
to produce the human readable version and
```
postcss --use=cssnext style-cssnext.css | cleancss > style.min.css
```
to make the minified version.
