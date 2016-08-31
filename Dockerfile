FROM alpine:latest
ADD . /tep.mit.edu

# set time zone 
ENV TZ=US/Eastern
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install git 
RUN apk --update add git && \
        rm -rf /var/lib/apt/lists/* && \
        rm /var/cache/apk/*

# setup hugo 

## this version of the site has been built with hugo 0.16
ENV HUGO_VERSION=0.16

## override this environment variable (BASE_URL="http://tep.mit.edu") 
## in order to properly deploy it to tep.mit.edu, etc. 
ENV BASE_URL=""

RUN apk add --update wget ca-certificates && \
  cd /tmp/ && \
  wget https://github.com/spf13/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_linux-64bit.tgz && \
  tar xzf hugo_${HUGO_VERSION}_linux-64bit.tgz && \
  rm -r hugo_${HUGO_VERSION}_linux-64bit.tgz && \
  mv hugo /usr/bin/hugo && \
  apk del wget ca-certificates && \
  rm /var/cache/apk/*

RUN git clone https://github.com/ggilmore/hugo-base16-theme /tep.mit.edu/themes/base16
WORKDIR /tep.mit.edu
EXPOSE 1313
CMD /usr/bin/hugo server --bind=0.0.0.0 --baseUrl=$BASE_URL

