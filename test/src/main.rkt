#lang racket

(require rackunit
         request/check
         "config.rkt")

(define auth-requester
  (add-requester-headers '("Authorization: Basic foo@bar.com:password")
                         (make-domain-requester auth-service-domain
                                                http-requester/exn)))

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
      (check-get "query-string-test?foo=bar" "Query param: bar")))
  (sleep 5)
  (test-case "Auth requests"
    (with-requester auth-requester
      (check-get "" "Hello!")
      (check-delete "database" "Bad idea!")
      (check-post "post-test" #"foo" "POSTed payload: foo")
      (check-put "put-test" #"foo" "PUTed payload: foo")
      (check-get "query-string-test?foo=bar" "Query param: bar"))))
