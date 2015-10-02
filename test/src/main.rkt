#lang racket

(require rackunit
         request/check
         "requester.rkt"
         "config.rkt")



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
