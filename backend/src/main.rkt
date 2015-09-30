#lang racket

(require spin
         web-server/http/request-structs)


(define request-body (compose bytes->string/utf-8 request-post-data/raw))

(get "/" (thunk "Hello!"))

(delete "/database" (thunk "Bad idea!"))

(post "/post-test" (lambda (req)
  (string-append "POSTed payload: " (request-body req ))))

(put "/put-test" (lambda (req)
  (string-append "PUTed payload: " (request-body req))))

(patch "/patch-test" (lambda (req)
  (string-append "PATCHed payload: " (request-body req))))

(module+ main
  (run #:listen-ip #f))
