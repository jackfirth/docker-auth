#lang racket

(require request/check
         "config.rkt")

(define auth-requester
  (make-domain-requester auth-service-domain
                         http-requester/exn))

(define backend-requester
  (make-domain-requester backend-service-domain
                         http-requester/exn))


(module+ test
  (with-requester backend-requester
    (check-get "" "Hello!")
    (check-delete "database" "Bad idea!")
    (check-post "post-test" #"foo" "POSTed payload: foo")
    (check-put "put-test" #"foo" "PUTed payload: foo")
    (check-get "query-string-test?foo=bar" "Query param: bar"))
  (with-requester auth-requester
    (check-get "" "Hello!")
    (check-delete "database" "Bad idea!")
    (check-post "post-test" #"foo" "POSTed payload: foo")
    (check-put "put-test" #"foo" "PUTed payload: foo")
    (check-get "query-string-test?foo=bar" "Query param: bar")))
