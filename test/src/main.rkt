#lang racket

(require fancy-app
         json
         rackunit
         request/check
         "config.rkt")

(define jsexpr->bytes/utf-8 (compose string->bytes/utf-8 jsexpr->string))

(define auth-base-requester
  (make-domain-requester auth-service-domain
                         http-requester/exn))

(define auth-proxy-requester/basic
  (add-requester-headers '("Authorization: Basic foo@bar.com:password")
                         auth-base-requester))

(define auth-proxy-requester/jwt
  (add-requester-headers (list (string-append "Authorization: Bearer " test-jwt))
                         auth-base-requester))

(define json-requester
  (compose (add-requester-headers '("Content-Type: application/json"
                                    "Accept: application/json") _)
           (wrap-requester-body jsexpr->bytes/utf-8 _)
           (wrap-requester-response string->jsexpr _)))

(define auth-api-requester
  (wrap-requester-location (string-append "auth/" _)
                           (json-requester auth-base-requester)))


(define backend-requester
  (make-domain-requester backend-service-domain
                         http-requester/exn))


(module+ test
  (test-case "Backend requests - no auth"
    (with-requester backend-requester
      (check-get "" "Hello!")
      (check-delete "database" "Bad idea!")
      (check-post "post-test" #"foo" "POSTed payload: foo")
      (check-put "put-test" #"foo" "PUTed payload: foo")
      (check-get "query-string-test?foo=bar" "Query param: bar")
      (check-get "identity-test" "No identity header")))
  (sleep 5)
  (test-case "Auth signup"
    (with-requester auth-api-requester
      (check-post-not-exn "signup" (hash 'email "foo@bar.com" 'password "password"))))
  (test-case "Basic auth requests"
    (with-requester auth-proxy-requester/basic
      (check-get "" "Hello!")
      (check-delete "database" "Bad idea!")
      (check-post "post-test" #"foo" "POSTed payload: foo")
      (check-put "put-test" #"foo" "PUTed payload: foo")
      (check-get "query-string-test?foo=bar" "Query param: bar")
      (check-get "identity-test" "Identity header: Email foo@bar.com")))
  (test-case "JWT auth requests"
    (with-requester auth-proxy-requester/jwt
      (check-get "" "Hello!")
      (check-delete "database" "Bad idea!")
      (check-post "post-test" #"foo" "POSTed payload: foo")
      (check-put "put-test" #"foo" "PUTed payload: foo")
      (check-get "query-string-test?foo=bar" "Query param: bar")
      (check-get "identity-test" "Identity header: Email foo@bar.com"))))
