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

## this version of the site has been built with hugo 0.18.1
ENV HUGO_VERSION=0.18.1

## override this environment variable (BASE_URL="http://tep.mit.edu") 
## in order to properly deploy it to tep.mit.edu, etc. 
ENV BASE_URL=""

RUN apk add --update wget ca-certificates && \
  cd /tmp/ && \
  wget https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
  tar -xvzf hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
  rm -r hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
  mv hugo_${HUGO_VERSION}_linux_amd64/hugo_${HUGO_VERSION}_linux_amd64 /usr/bin/hugo && \ 
  apk del wget ca-certificates && \
  rm /var/cache/apk/*

RUN git clone https://github.com/ggilmore/hugo-base16-theme /tep.mit.edu/themes/base16
WORKDIR /tep.mit.edu
EXPOSE 80
CMD /usr/bin/hugo server --bind=0.0.0.0 \ 
  -p 80 \
  --appendPort=false \
  --baseUrl=$BASE_URL 

