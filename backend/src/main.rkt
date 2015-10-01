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

(get "/query-string-test" (lambda (req)
  (string-append "Query param: " (params req 'foo))))

(get "/identity-test" (lambda (req)
  (define identity (headers-assq* #"Identity" (request-headers/raw req)))
  (if identity
      (string-append "Identity header: " (bytes->string/utf-8 identity))
      (string-append "No identity header"))))

(module+ main
  (run #:listen-ip #f))
