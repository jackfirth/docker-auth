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

(define ((header-test-route header-name) req)
  (define header-name/bytes (string->bytes/utf-8 header-name))
  (define header (headers-assq* header-name/bytes (request-headers/raw req)))
  (if header
      (format "~a header: ~a"
              header-name
              (bytes->string/utf-8 (header-value header)))
      (format "No ~a header"
              header-name)))


(get "/identity-test" (header-test-route "Identity"))
(get "/content-type-test" (header-test-route "Content-Type"))
(get "/accept-test" (header-test-route "Accept"))

(module+ main
  (run #:listen-ip #f))
