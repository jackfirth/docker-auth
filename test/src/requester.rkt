#lang racket

(provide auth-proxy-requester/basic
         auth-proxy-requester/jwt
         auth-api-requester
         backend-requester)

(require fancy-app
         json
         request
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
